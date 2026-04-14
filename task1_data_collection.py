import requests
import json
import os
import time
from datetime import datetime

# Settings
BASE_URL = "https://hacker-news.firebaseio.com/v0"
UA_HEADER = {"User-Agent": "TrendPulse/1.0"}
MAX_PER_CAT = 25

# Our keyword lists for sorting stories
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm", "programming", "developer", "open source", "github", "linux", "python", "javascript", "startup", "app", "tool", "framework", "model", "neural", "robot", "automation", "chip", "hardware", "server", "database", "security", "cyber", "hack", "vulnerability", "exploit", "patch", "release", "launch", "platform", "saas", "devops", "docker", "kubernetes", "rust", "typescript", "web", "browser", "mobile", "ios", "android"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global", "political", "policy", "military", "conflict", "treaty", "sanction", "diplomat", "minister", "parliament", "senate", "congress", "law", "court", "judge", "tariff", "trade", "border", "refugee", "protest", "democracy", "economy", "inflation", "recession", "tax", "bank", "fed", "dollar", "ukraine", "china", "russia", "europe", "middle east", "africa", "india", "nuclear", "weapon"],
    "sports": ["nfl", "nba", "fifa", "sport", "team", "player", "league", "championship", "tournament", "olympic", "athlete", "coach", "match", "score", "win", "loss", "transfer", "draft", "season", "playoff", "super bowl", "world cup", "cricket", "tennis", "golf", "football", "soccer", "baseball", "hockey", "swimming", "marathon", "race", "record", "stadium", "fan", "jersey"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome", "scientist", "experiment", "lab", "quantum", "climate", "ocean", "planet", "star", "galaxy", "black hole", "vaccine", "medicine", "cancer", "gene", "dna", "rna", "cell", "evolution", "fossil", "dinosaur", "telescope", "particle", "chemistry", "element", "material", "battery", "energy", "solar", "fusion", "neuron", "brain", "psychology", "math"],
    "entertainment": ["movie", "film", "music", "netflix", "book", "show", "award", "streaming", "album", "song", "artist", "actor", "director", "box office", "trailer", "review", "concert", "tour", "band", "tv", "series", "episode", "season", "anime", "manga", "comic", "game", "gaming", "playstation", "xbox", "nintendo", "steam", "podcast", "youtube", "tiktok", "instagram", "celebrity", "oscar", "grammy", "emmy", "golden globe", "disney", "marvel"]
}

def get_category_label(title):
    # check title against keywords
    t = title.lower()
    for cat, keywords in CATEGORIES.items():
        for k in keywords:
            if k in t:
                return cat
    return None

def get_hn_ids():
    # pull from top and best stories to get a bigger sample
    endpoints = ["topstories", "beststories"]
    all_ids = []

    for ep in endpoints:
        try:
            r = requests.get(f"{BASE_URL}/{ep}.json", headers=UA_HEADER, timeout=10)
            if r.status_code == 200:
                data = r.json()[:500]
                all_ids.extend(data)
                print(f"Fetched {len(data)} IDs from {ep}")
        except Exception as e:
            print(f"Error fetching {ep}: {e}")

    # deduplicate but keep original order
    return list(dict.fromkeys(all_ids))

def run_collection():
    ids_to_check = get_hn_ids()
    results = []
    counts = {k: 0 for k in CATEGORIES.keys()}
    slept_for = {k: False for k in CATEGORIES.keys()}

    now_ts = datetime.now().isoformat(timespec="seconds")

    print("\nStarting story processing...")

    for sid in ids_to_check:
        # stop if we hit our goals
        if all(c >= MAX_PER_CAT for c in counts.values()):
            print("Reached limits for all categories.")
            break

        try:
            res = requests.get(f"{BASE_URL}/item/{sid}.json", headers=UA_HEADER, timeout=10)
            item = res.json()

            if not item or item.get("type") != "story":
                continue

            title = item.get("title", "").strip()
            cat = get_category_label(title)

            if cat and counts[cat] < MAX_PER_CAT:
                # format specific record for task
                entry = {
                    "post_id": item.get("id"),
                    "title": title,
                    "category": cat,
                    "score": item.get("score", 0),
                    "num_comments": item.get("descendants", 0),
                    "author": item.get("by", "unknown"),
                    "collected_at": now_ts
                }
                results.append(entry)
                counts[cat] += 1

                print(f"  [{cat}] {counts[cat]}/{MAX_PER_CAT}: {title[:50]}...")

                # specific requirement: sleep 2s after finishing a category
                if counts[cat] == MAX_PER_CAT and not slept_for[cat]:
                    print(f"Finished {cat}, pausing 2s...")
                    time.sleep(2)
                    slept_for[cat] = True

        except Exception:
            continue # skip errors

    return results

def main():
    print("=== TrendPulse Task 1 ===")
    data = run_collection()

    if not data:
        print("No data found.")
        return

    # setup folder and filename
    if not os.path.exists("data"):
        os.makedirs("data")

    fn = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSuccess: Collected {len(data)} stories.")
    print(f"Saved to {fn}")

if __name__ == "__main__":
    main()
