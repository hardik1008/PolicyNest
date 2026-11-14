"""PolicyNest Onboarding Copilot proxy.

A tiny HTTP server that holds the Anthropic API key (env var ANTHROPIC_API_KEY) so the
browser never sees it. The static site POSTs {question, context, passages, history} to
/api/copilot; this adds the system prompt and guardrails and calls Claude.

Deployed as its own Embarko server app (static sites cannot hold env vars).
Run locally:  ANTHROPIC_API_KEY=... python main.py   (reads PORT, default 8787)
"""
import json
import os
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


def ask(body):
    import anthropic  # imported lazily so /health works without the SDK
    passages = body.get("passages") or []
    ptext = "\n\n".join(
        f"[{p.get('cite', p.get('src', '?'))}]\n{str(p.get('text', ''))[:2400]}" for p in passages[:6])
    state = json.dumps(body.get("context") or {}, ensure_ascii=False)[:6000]
    msgs = []
    for turn in (body.get("history") or [])[-6:]:
        if turn.get("role") in ("user", "assistant") and turn.get("text"):
            msgs.append({"role": turn["role"], "content": str(turn["text"])[:1500]})
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if msgs and msgs[-1]["role"] == "user":
        msgs.pop()
    q = str(body.get("question", ""))[:1200]
    msgs.append({"role": "user", "content": f"APP_STATE:\n{state}\n\nPASSAGES:\n{ptext}\n\nQUESTION:\n{q}"})
    client = anthropic.Anthropic()
    kw = dict(model=MODEL, max_tokens=1500, system=SYSTEM, messages=msgs, output_config={"effort": EFFORT})
    try:
        r = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kw)
    except (anthropic.BadRequestError, TypeError):
        r = client.messages.create(**kw)  # model or SDK without server-side fallback support
    if r.stop_reason == "refusal":
        return "I can't help with that one. Ask me about your documents, the steps, or what to fix next."
    return "".join(b.text for b in r.content if b.type == "text").strip()


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
            answer = ask(body)
            _day["n"] += 1
            return self._json(200, {"answer": answer, "model": MODEL, "daily_left": _daily_left()})
        except Exception as e:  # never leak the key or stack to the browser
            return self._json(502, {"error": "upstream", "type": type(e).__name__})

    def log_message(self, fmt, *args):  # no request bodies in logs
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
