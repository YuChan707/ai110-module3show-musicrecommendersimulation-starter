from .recommender import load_songs, recommend_songs
import os


def main() -> None:
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(data_path)

    profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "energetic", "energy": 0.90}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.45}),
        ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.95}),
    ]

    for name, prefs in profiles:
        print(f"\n===== {name} =====")
        for i, result in enumerate(recommend_songs(prefs, songs, k=5), 1):
            song = result["song"]
            print(f"{i}. {song['title']} by {song['artist']} - score {result['score']}")
            print(f"   reasons: {', '.join(result['reasons'])}")


if __name__ == "__main__":
    main()