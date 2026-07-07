"""Phase 05 Integration: Stranger Things — imports, math, datetime, file I/O, pathlib, JSON, CSV, regex."""

import csv
import json
import math
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean, stdev

TMP_DIR = Path("/tmp/stranger-things-analysis")
CSV_PATH = TMP_DIR / "episodes.csv"
JSON_PATH = TMP_DIR / "analysis.json"
TRANSCRIPT_PATH = TMP_DIR / "transcripts.txt"


def setup_data():
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    episodes = [
        ["season", "episode", "title", "duration_min", "rating", "air_date"],
        [1, 1, "The Vanishing of Will Byers", 47, 8.7, "2016-07-15"],
        [1, 2, "The Weirdo on Maple Street", 55, 8.5, "2016-07-15"],
        [1, 3, "Holly, Jolly", 51, 8.8, "2016-07-22"],
        [1, 4, "The Body", 49, 8.6, "2016-07-29"],
        [1, 5, "The Flea and the Acrobat", 52, 8.7, "2016-08-05"],
        [1, 6, "The Monster", 46, 8.9, "2016-08-12"],
        [1, 7, "The Bathtub", 48, 8.8, "2016-08-19"],
        [1, 8, "The Upside Down", 55, 9.0, "2016-08-26"],
        [2, 1, "MADMAX", 48, 8.8, "2017-10-27"],
        [2, 2, "Trick or Treat, Freak", 56, 8.7, "2017-10-27"],
        [2, 3, "The Pollywog", 51, 8.8, "2017-11-03"],
        [2, 4, "Will the Wise", 50, 8.9, "2017-11-10"],
        [2, 5, "Dig Dug", 52, 8.7, "2017-11-17"],
        [2, 6, "The Spy", 48, 8.8, "2017-11-24"],
        [2, 7, "The Lost Sister", 47, 7.1, "2017-11-24"],
        [2, 8, "The Mind Flayer", 52, 9.1, "2017-11-24"],
        [2, 9, "The Gate", 63, 9.2, "2017-11-24"],
        [3, 1, "Suzie, Do You Copy?", 50, 8.6, "2019-07-04"],
        [3, 2, "The Mall Rats", 50, 8.5, "2019-07-04"],
        [3, 3, "The Case of the Missing Lifeguard", 52, 8.4, "2019-07-04"],
        [3, 4, "The Sauna Test", 50, 8.8, "2019-07-04"],
        [3, 5, "The Flayed", 52, 8.6, "2019-07-04"],
        [3, 6, "E Pluribus Unum", 59, 8.7, "2019-07-04"],
        [3, 7, "The Bite", 59, 9.0, "2019-07-04"],
        [3, 8, "The Battle of Starcourt", 78, 9.3, "2019-07-04"],
    ]
    with open(CSV_PATH, "w", newline="") as f:
        csv.writer(f).writerows(episodes)

    transcripts = [
        "Eleven uses her telekinesis to flip the van.",
        "Dustin says: 'She's our friend, and she's crazy!'",
        "Hopper digs through the Upside Down in the lab.",
        "Steve hits the Demo-dog with his nail bat. Thwack!",
        "Vecna whispers: 'Your little friend is gone.'",
        "Nancy shoots the Demogorgon with the rifle.",
        "Max runs from Vecna into the Creel house. 1986.",
        "Mike tells Eleven: 'I love you, but you don't have to say it back.'",
    ]
    TRANSCRIPT_PATH.write_text("\n".join(transcripts))
    print(f"Created {len(episodes) - 1} episodes")


def load_episodes():
    episodes = []
    with open(CSV_PATH) as f:
        for row in csv.DictReader(f):
            row["season"] = int(row["season"])
            row["episode"] = int(row["episode"])
            row["duration_min"] = int(row["duration_min"])
            row["rating"] = float(row["rating"])
            episodes.append(row)
    return episodes


def analyze_ratings(episodes):
    ratings = [ep["rating"] for ep in episodes]
    return {"count": len(ratings), "mean": round(mean(ratings), 2), "stdev": round(stdev(ratings), 2) if len(ratings) > 1 else 0, "min": min(ratings), "max": max(ratings)}


def calculate_watch_time(episodes):
    total_minutes = sum(ep["duration_min"] for ep in episodes)
    delta = timedelta(minutes=total_minutes)
    start = datetime(2024, 1, 1, 20, 0)
    return {"total_hours": round(total_minutes / 60, 2), "duration_str": str(delta), "end": (start + delta).strftime("%H:%M")}


def pick_random_episode(episodes):
    ep = random.choice(episodes)
    return f"S{ep['season']}E{ep['episode']} \"{ep['title']}\" ({ep['rating']})"


def search_transcripts(pattern):
    return re.findall(pattern, TRANSCRIPT_PATH.read_text(), re.IGNORECASE)


def season_summary(episodes):
    seasons = {}
    for ep in episodes:
        s = ep["season"]
        seasons.setdefault(s, {"count": 0, "total_min": 0, "ratings": []})
        seasons[s]["count"] += 1
        seasons[s]["total_min"] += ep["duration_min"]
        seasons[s]["ratings"].append(ep["rating"])
    return {f"S{s}": {"episodes": info["count"], "hours": round(info["total_min"] / 60, 2), "avg_rating": round(mean(info["ratings"]), 2)} for s, info in seasons.items()}


def save_analysis(analysis):
    with open(JSON_PATH, "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"Analysis saved to {JSON_PATH}")


def main():
    setup_data()
    episodes = load_episodes()
    print(f"Loaded {len(episodes)} episodes")
    ratings = analyze_ratings(episodes)
    print(f"Ratings: mean={ratings['mean']}, σ={ratings['stdev']}, range={ratings['min']}-{ratings['max']}")
    watch = calculate_watch_time(episodes)
    print(f"Watch time: {watch['total_hours']}h (ends {watch['end']})")
    print(f"Random pick: {pick_random_episode(episodes)}")
    names = search_transcripts(r"[A-Z][a-z]+")
    print(f"Character names found: {len(names)}")
    summary = season_summary(episodes)
    save_analysis({"ratings": ratings, "watch_time": watch, "seasons": summary, "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    import shutil
    shutil.rmtree(TMP_DIR)
    print(f"Cleaned up {TMP_DIR}")


if __name__ == "__main__":
    main()
