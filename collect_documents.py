import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://api.pullpush.io/reddit/search"
HEADERS = {"User-Agent": "unofficial-guide-class-project/0.1"}
OUT_DIR = Path("documents")

THREADS = [
    ("southside_safety", "1402pj4"),
    ("avoid_sterling", "10qpclk"),
    ("housing_costs", "1c4013y"),
    ("housing_scams", "12ew1tz"),
    ("lease_dispute", "1580z76"),
    ("roommates", "1ko80eo"),
    ("identity_logan_park", "1abwegr"),
    ("avoid_ace_berkeley", "1idyoyy"),
    ("best_neighborhoods", "vcd6uu"),
    ("neighborhoods_cs", "ne41wq"),
    ("solo_rooms", "1k6ezhe"),
    ("grad_housing", "1irtkg6"),
    ("coops", "1koq3t3"),
    ("when_to_search", "1i3kdjh"),
    ("new_student_housing", "r01hx"),
    ("intl_summer_housing", "1dup8e"),
    ("rent_hike", "1kmzn6q"),
]


def get_json(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(30 * (attempt + 1))
                continue
            raise


def get_submissions(ids):
    params = urllib.parse.urlencode({"ids": ",".join(ids)})
    return get_json(f"{BASE}/submission/?{params}").get("data", [])


def get_comments(link_id):
    params = urllib.parse.urlencode({
        "link_id": link_id,
        "size": 30,
        "sort_type": "score",
        "sort": "desc",
    })
    return get_json(f"{BASE}/comment/?{params}").get("data", [])


def usable_text(text):
    if not text:
        return False
    return text.strip() not in ("[removed]", "[deleted]", "")


def write_document(slug, sub, comments):
    lines = []
    lines.append(f"Title: {sub['title']}")
    lines.append(f"Source: r/berkeley thread, https://www.reddit.com{sub['permalink']}")
    lines.append(f"Posted: {time.strftime('%Y-%m-%d', time.gmtime(sub['created_utc']))}")
    lines.append("")
    if usable_text(sub.get("selftext")):
        lines.append("Original post:")
        lines.append(sub["selftext"].strip())
        lines.append("")
    lines.append("Replies from students:")
    kept = 0
    for c in comments:
        body = c.get("body", "")
        if not usable_text(body):
            continue
        if c.get("author") == "AutoModerator":
            continue
        if len(body.strip()) < 40:
            continue
        lines.append("")
        lines.append(f"[{c.get('score', 0)} points] {body.strip()}")
        kept += 1
        if kept >= 20:
            break
    path = OUT_DIR / f"{slug}_{sub['id']}.txt"
    path.write_text("\n".join(lines))
    print(f"wrote {path} ({kept} comments kept)")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    missing = [(slug, tid) for slug, tid in THREADS if not (OUT_DIR / f"{slug}_{tid}.txt").exists()]
    if not missing:
        print("all documents already collected")
        return
    subs = {s["id"]: s for s in get_submissions([tid for _, tid in missing])}
    time.sleep(10)
    for slug, tid in missing:
        sub = subs.get(tid)
        if sub is None:
            print(f"could not fetch thread {tid} for {slug}")
            continue
        try:
            comments = get_comments(tid) if sub.get("num_comments", 0) > 0 else []
            write_document(slug, sub, comments)
            time.sleep(10)
        except Exception as e:
            print(f"failed on {slug}: {e}")


if __name__ == "__main__":
    main()
