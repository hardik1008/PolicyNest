"""Shared helpers: read the PS-01 workbooks with the standard library only (an .xlsx is a zip of XML)."""
import os, sys, csv, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xl import read as read_xlsx

APPS_XLSX = os.environ.get('PS01_APPS', r'D:\PS-01_posp_applications.xlsx')
DOCS_XLSX = os.environ.get('PS01_DOCS', r'D:\PS-01_document_review_test_set.xlsx')
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tables'))
EPOCH = dt.datetime(1899, 12, 30)


def sheet(book, name):
    rows = book[name]
    h = rows[0]
    return [dict(zip(h, r + [''] * (len(h) - len(r)))) for r in rows[1:]]


def serial(v):
    """Excel serial number (days) -> float, or None when blank."""
    return float(v) if v not in ('', None) else None


def to_dt(v):
    s = serial(v)
    return None if s is None else EPOCH + dt.timedelta(days=s)


def pct(sorted_vals, p):
    """Linear-interpolation percentile (numpy default), p in 0..100."""
    n = len(sorted_vals)
    if n == 0:
        return None
    k = (n - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, n - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def median(v):
    return pct(sorted(v), 50)


def write_csv(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
