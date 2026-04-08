"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
import os


def main() -> None:
    """Run the CLI-first recommendation simulation."""
    # Get the path to data/songs.csv relative to this script
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(data_path) 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for result in recommendations:
        song    = result["song"]
        score   = result["score"]
        reasons = result["reasons"]
        print(f"{song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"Why: {', '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()

profiles = [
    ("High-Energy Pop", {"genre": "pop", "mood": "energetic", "energy": 0.90}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.45}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.95}),
]

for name, prefs in profiles:
    print(f"\n===== {name} =====")
    recs = recommend_songs(prefs, songs, k=5)
    for i, result in enumerate(recs, 1):
        song = result["song"]
        print(f"{i}. {song['title']} by {song['artist']} - score {result['score']}")
        print(f"   reasons: {', '.join(result['reasons'])}")
