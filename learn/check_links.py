import json, os, ssl, sys
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
cats = []
for p in ("part1.json", "part2.json", "part3.json"):
    with open(os.path.join(HERE, "links", p), encoding="utf-8") as f:
        cats.extend(json.load(f))

json.dump(cats, open(os.path.join(HERE, "links", "all.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def probe(url, method):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return r.status, r.geturl()


def check(item):
    url = item["u"]
    last = ""
    for method in ("HEAD", "GET"):
        try:
            status, final = probe(url, method)
            return (url, status, final, "")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (403, 405, 406, 429) and method == "HEAD":
                continue
            if e.code in (403, 429):
                return (url, e.code, url, last)
            return (url, e.code, url, last)
        except Exception as e:
            last = type(e).__name__ + ": " + str(e)[:70]
    return (url, 0, url, last)


items = [it for c in cats for it in c["items"]]
print(f"{len(cats)} categories, {len(items)} links\n", flush=True)

seen = {}
for it in items:
    seen.setdefault(it["u"], []).append(it["t"])
dupes = {u: t for u, t in seen.items() if len(t) > 1}
if dupes:
    print("DUPLICATE URLS:")
    for u, t in dupes.items():
        print("  ", u, "->", t)
    print()

with ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(check, items))

bad = []
for (url, status, final, err), it in zip(results, items):
    ok = 200 <= status < 400
    if not ok:
        bad.append((status or "ERR", url, it["t"], err))
    elif final.rstrip("/") != url.rstrip("/"):
        print(f"  redirect  {url}\n         -> {final}")

print(f"\n{len(items) - len(bad)}/{len(items)} OK")
if bad:
    print("\nFAILED:")
    for status, url, title, err in sorted(bad, key=lambda x: str(x[0])):
        print(f"  [{status}] {title}\n        {url}  {err}")
