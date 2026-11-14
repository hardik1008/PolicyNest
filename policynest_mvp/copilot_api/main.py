"""PolicyNest Onboarding Copilot proxy.

A tiny HTTP server that holds the Anthropic API key (env var ANTHROPIC_API_KEY) so the
browser never sees it. The static site POSTs {question, context, history} to /api/copilot.
This server looks up the rulebook passages itself (BM25 over the applicant-safe kb.json that
build_site.py writes next to this file), checks the context against a fixed schema, refuses
ID numbers, calls Claude and filters the answer (ADR 0002). Passages sent by a browser are ignored.

Deployed as its own Embarko server app (static sites cannot hold env vars).
Run locally:  ANTHROPIC_API_KEY=... python main.py   (reads PORT, default 8787)
"""
import json
import math
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Local runs: read ../../.env if present (Embarko sets real env vars and never gets .env).
_here = Path(__file__).resolve()
for envfile in [p / ".env" for p in (_here.parent, *_here.parents[1:3])]:
    if envfile.is_file():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

MODEL = os.environ.get("COPILOT_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("COPILOT_EFFORT", "low")
# Production (Embarko sets APP_NAME) allows only the live site; local runs also allow the dev server.
# The "null" origin (a page opened from file://) is never allowed (G-24).
_default_origins = "https://policynest.embarko.app" + ("" if os.environ.get("APP_NAME") else ",http://localhost:8000,http://127.0.0.1:8000")
ALLOWED = {o.strip() for o in os.environ.get("COPILOT_ORIGINS", _default_origins).split(",") if o.strip() and o.strip() != "null"}
MAX_BODY = 24_000
RATE = (20, 600)  # 20 questions per 10 minutes per client
GLOBAL_PER_MIN = int(os.environ.get("COPILOT_GLOBAL_PER_MIN", "30"))  # all clients together (fallback if the client address is unreliable)
DAILY_CAP = int(os.environ.get("COPILOT_DAILY_CAP", "50"))  # AI answers per UTC day (G-25, user decision 14 Nov)
_hits = {}
_global = []
_day = {"date": "", "n": 0}

SYSTEM = """You are the PolicyNest Onboarding Copilot. You help an applicant become a POSP (Point of Sales Person) insurance agent with PolicyNest, a broker. You guide them through: their details, six documents (PAN card, Aadhaar, Class 10 or 12 marksheet, bank proof such as a cancelled cheque or passbook, a selfie), verification, 15 hours of training, the exam, and the certificate.

You receive the applicant's live progress (APP_STATE) and passages from PolicyNest's rulebook and reference documents (PASSAGES). Use them.

Rules you must follow:
- Answer in plain, short, friendly language (aim for under 120 words). Use numbered steps when telling them what to do. Reply in Hindi if they write in Hindi or ask for Hindi.
- Base rule statements only on PASSAGES. Cite the source in square brackets, e.g. [Rulebook §4.1]. If the passages do not cover it, say you are not sure and suggest they ask a reviewer through the app. Never invent rules, numbers, fees or timelines.
- Never decide or predict the outcome. Do not say they are approved, rejected, eligible or ineligible; the verification engine and human reviewers decide.
- Never use words like fraud, fake, forged, suspicious or tampered. Describe problems neutrally ("the name doesn't match the PAN card").
- Never ask for, repeat or guess full PAN, Aadhaar, bank account numbers or passwords. If they type one, tell them not to share it here.
- Stay on PolicyNest onboarding. Politely decline anything else.
- Remember that PAN, bank penny-drop, face match and IRDAI registry checks in this demo are simulated."""


def _cors(h, origin):
    if origin in ALLOWED:
        h.send_header("Access-Control-Allow-Origin", origin)
        h.send_header("Vary", "Origin")
        h.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        h.send_header("Access-Control-Allow-Headers", "Content-Type")


def _client(h):
    """The client address the edge proxy saw. A client can put anything at the left of X-Forwarded-For,
    so only entries appended by Embarko's own proxies are trusted (G-24). Measured 14 Nov: Embarko's two proxy
    hops append two entries ([client, edge]; a spoofed header becomes [spoof, client, edge]), so the client
    is the second entry from the right. XFF_TRUSTED_HOPS overrides this if Embarko changes."""
    hops = int(os.environ.get("XFF_TRUSTED_HOPS", "2"))
    xff = [p.strip() for p in (h.headers.get("X-Forwarded-For") or "").split(",") if p.strip()]
    return xff[-hops] if len(xff) >= hops else h.client_address[0]


def _limited(ip):
    now = time.time()
    if len(_hits) > 5000:  # prune entries with no recent questions
        for k in [k for k, v in _hits.items() if not v or now - v[-1] >= RATE[1]]:
            _hits.pop(k, None)
    _global[:] = [t for t in _global if now - t < 60]
    q = [t for t in _hits.get(ip, []) if now - t < RATE[1]]
    if len(q) >= RATE[0] or len(_global) >= GLOBAL_PER_MIN:
        _hits[ip] = q
        return True
    q.append(now)
    _hits[ip] = q
    _global.append(now)
    return False


def _daily_left():
    today = time.strftime("%Y-%m-%d", time.gmtime())
    if _day["date"] != today:
        _day.update(date=today, n=0)
    return max(0, DAILY_CAP - _day["n"])


def _key_ok():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    return bool(k) and not k.startswith("your-")


# ---------- Retrieval: the same BM25 the browser uses, over applicant-safe passages only ----------
_STOP = set("the and for are you your is of to in on a an it be or my me i we do does what how why can this that with not".split())


def tokens(s):
    s = re.sub(r"[^a-z0-9ऀ-ॿ ]+", " ", str(s).lower())
    return [w for w in s.split() if len(w) > 1 and w not in _STOP]


def load_kb(path=_here.parent / "kb.json"):
    try:
        kb = [c for c in json.loads(Path(path).read_text(encoding="utf-8")) if c.get("audience") == "applicant"]
    except (OSError, ValueError):
        kb = []
    df = {}
    for c in kb:
        c["_tk"] = tokens(c["head"] + " " + c["head"] + " " + c["text"])
        for t in set(c["_tk"]):
            df[t] = df.get(t, 0) + 1
    n = len(kb)
    idf = {t: math.log(1 + (n - d + .5) / (d + .5)) for t, d in df.items()}
    avg = sum(len(c["_tk"]) for c in kb) / max(1, n)
    return {"chunks": kb, "idf": idf, "avg": avg}


KB = load_kb()


def retrieve(q, n=5, kb=None):
    kb = kb or KB
    qt, k1, b, out = tokens(q), 1.4, .75, []
    for c in kb["chunks"]:
        tf = {}
        for t in c["_tk"]:
            tf[t] = tf.get(t, 0) + 1
        s = sum(kb["idf"].get(t, 0) * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(c["_tk"]) / kb["avg"]))
                for t in qt if t in tf)
        if s > 0:
            out.append((s, c))
    return [c for s, c in sorted(out, key=lambda x: -x[0])[:n]]


# ---------- Input checks ----------
ID_NUMBER = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b|\b[A-Za-z]{5}\d{4}[A-Za-z]\b|\b\d{9,18}\b")
CODE = re.compile(r"^[A-Za-z0-9_:\- ]{1,40}$")


def _s(v, n):
    return str(v)[:n] if isinstance(v, (str, int, float)) and not isinstance(v, bool) else None


def _i(v):
    return int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def clean_context(ctx):
    """Keep only the fields the page sends (copilotContext in PolicyNest.html), with types and lengths
    checked. Anything else is dropped, so a caller cannot smuggle free text into the prompt."""
    ctx = ctx if isinstance(ctx, dict) else {}
    out = {"first_name": re.sub(r"[^A-Za-zऀ-ॿ .'-]", "", _s(ctx.get("first_name"), 40) or "") or None}
    for k, n in (("stage", 40), ("details_page", 60), ("application_status", 40), ("decision", 40),
                 ("suggested_next_step", 300)):
        out[k] = _s(ctx.get(k), n)
    for k in ("minutes_left_in_sitting", "sittings", "round", "exam_score"):
        out[k] = _i(ctx.get(k))
    th = ctx.get("training_hours")
    out["training_hours"] = th if isinstance(th, (int, float)) and not isinstance(th, bool) else None
    docs = []
    for d in (ctx.get("documents") or [])[:6] if isinstance(ctx.get("documents"), list) else []:
        if isinstance(d, dict):
            docs.append({"document": _s(d.get("document"), 40), "status": _s(d.get("status"), 20),
                         "refusal_reason": _s(d.get("refusal_reason"), 200),
                         "open_issues": [x for x in (d.get("open_issues") or [])[:8]
                                         if isinstance(x, str) and CODE.match(x)]})
    out["documents"] = docs
    fu = ctx.get("follow_up_items") if isinstance(ctx.get("follow_up_items"), list) else []
    out["follow_up_items"] = [{"document": _s(i.get("document"), 40), "issue": _s(i.get("issue"), 40)}
                              for i in fu[:10] if isinstance(i, dict)]
    fe = ctx.get("field_errors") if isinstance(ctx.get("field_errors"), list) else []
    out["field_errors"] = [x for x in fe[:12] if isinstance(x, str) and CODE.match(x)]
    return out


def clean_history(hist):
    msgs = []
    for turn in (hist if isinstance(hist, list) else [])[-6:]:
        if isinstance(turn, dict) and turn.get("role") in ("user", "assistant") and isinstance(turn.get("text"), str):
            msgs.append({"role": turn["role"], "content": turn["text"][:800]})
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if msgs and msgs[-1]["role"] == "user":
        msgs.pop()
    return msgs


def has_id_number(body):
    texts = [str(body.get("question", ""))] + [t.get("text", "") for t in (body.get("history") or [])
                                              if isinstance(t, dict) and t.get("role") == "user"]
    ctx = body.get("context") if isinstance(body.get("context"), dict) else {}
    texts += [str(ctx.get("suggested_next_step", ""))] + [str(d.get("refusal_reason", "")) for d in
                                                         (ctx.get("documents") or []) if isinstance(d, dict)]
    return any(ID_NUMBER.search(str(t)) for t in texts)


# ---------- Output filter (the page has the same one; this is the second line) ----------
BANNED_OUT = re.compile(r"\b(fraud\w*|fake|forged|tamper\w*|suspicious)\b|\byou (are|have been) (approved|rejected)\b", re.I)
SAFE = ("I can't say how your application will be decided; the verification checks and our team do that. "
        "Ask me about your documents, the steps, or what to fix next.")
REFUSED = "I can't help with that one. Ask me about your documents, the steps, or what to fix next."


def build_request(body):
    """Pure: the model request and the citations, from the request body. Passages from the body are ignored."""
    ctx = clean_context(body.get("context"))
    q = str(body.get("question", ""))[:1200]
    hits = retrieve(q + (" document photo upload" if "document" in (ctx.get("stage") or "").lower() else ""))
    ptext = "\n\n".join(f"[{c['cite']}]\n{c['text'][:2400]}" for c in hits)
    msgs = clean_history(body.get("history"))
    msgs.append({"role": "user", "content": f"APP_STATE:\n{json.dumps(ctx, ensure_ascii=False)}\n\n"
                                            f"PASSAGES:\n{ptext}\n\nQUESTION:\n{q}"})
    kw = dict(model=MODEL, max_tokens=1500, system=SYSTEM, messages=msgs, output_config={"effort": EFFORT})
    return kw, [c["cite"] for c in hits]


def call_model(kw):
    """Returns (stop_reason, text). Opus and Sonnet get Anthropic's server-side refusal fallback;
    Haiku 5.5 has none, so it is called plainly."""
    import anthropic  # imported lazily so /health and the tests work without the SDK
    client = anthropic.Anthropic()
    if kw["model"].startswith("claude-haiku"):
        r = client.messages.create(**kw)
    else:
        try:
            r = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kw)
        except (anthropic.BadRequestError, TypeError):
            r = client.messages.create(**kw)  # model or SDK without server-side fallback support
    return r.stop_reason, "".join(b.text for b in r.content if b.type == "text").strip()


def ask(body):
    kw, cites = build_request(body)
    stop, text = call_model(kw)
    if stop == "refusal":
        return REFUSED, cites
    if not text or BANNED_OUT.search(text):
        return SAFE, cites
    return text, cites


class H(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        _cors(self, self.headers.get("Origin", ""))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        _cors(self, self.headers.get("Origin", ""))
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/health") or self.path == "/":
            xff = [p for p in (self.headers.get("X-Forwarded-For") or "").split(",") if p.strip()]
            # xff_hops lets us check how the edge builds X-Forwarded-For (no addresses are returned)
            return self._json(200, {"ok": True, "llm": _key_ok(), "model": MODEL, "daily_left": _daily_left(),
                                    "daily_cap": DAILY_CAP, "xff_hops": len(xff)})
        self._json(404, {"error": "not_found"})

    def do_POST(self):
        if not self.path.startswith("/api/copilot"):
            return self._json(404, {"error": "not_found"})
        origin = self.headers.get("Origin", "")
        if origin not in ALLOWED:
            return self._json(403, {"error": "origin_not_allowed"})
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BODY:
            return self._json(413, {"error": "body_too_large"})
        if _limited(_client(self)):
            return self._json(429, {"error": "rate_limited"})
        if not _key_ok():
            return self._json(503, {"error": "no_key"})
        if _daily_left() <= 0:
            return self._json(429, {"error": "daily_cap"})
        try:
            body = json.loads(self.rfile.read(n))
        except ValueError:
            return self._json(400, {"error": "bad_json"})
        if not isinstance(body, dict) or not str(body.get("question", "")).strip():
            return self._json(400, {"error": "schema"})
        if has_id_number(body):  # rulebook §4.3: never send ID numbers to a model
            return self._json(400, {"error": "id_number"})
        try:
            answer, cites = ask(body)
            _day["n"] += 1
            return self._json(200, {"answer": answer, "sources": cites, "model": MODEL, "daily_left": _daily_left()})
        except Exception as e:  # never leak the key or stack to the browser
            return self._json(502, {"error": "upstream", "type": type(e).__name__})

    def log_message(self, fmt, *args):  # no request bodies in logs
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
