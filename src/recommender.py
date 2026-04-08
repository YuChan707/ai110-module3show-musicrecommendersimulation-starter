from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        def score(song: Song) -> float:
            genre_score   = 1.0 if song.genre == user.favorite_genre else 0.0
            mood_score    = 1.0 if song.mood  == user.favorite_mood  else 0.0
            energy_score  = 1.0 - abs(song.energy - user.target_energy)
            acoustic_score = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness

            return (
                genre_score    * 0.30 +
                mood_score     * 0.25 +
                energy_score   * 0.25 +
                acoustic_score * 0.20
            )

        return sorted(self.songs, key=score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({song.genre})")

        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood ({song.mood})")

        if abs(song.energy - user.target_energy) < 0.15:
            reasons.append("energy level is close to your target")

        acoustic_score = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness
        if acoustic_score > 0.7:
            reasons.append("fits your acoustic preference")

        if reasons:
            return "Recommended because it " + " and ".join(reasons)
        return "Closest available match to your preferences"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def score_song(song: Dict) -> Tuple[float, str]:
        # --- Rule 1: Genre match (30%) ---
        genre_score = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0

        # --- Rule 2: Mood match (25%) ---
        mood_score = 1.0 if song["mood"] == user_prefs.get("mood") else 0.0

        # --- Rule 3: Energy proximity (25%) ---
        target_energy = user_prefs.get("energy", 0.5)
        energy_diff = abs(song["energy"] - target_energy)
        energy_score = 1.0 - energy_diff

        # --- Rule 4: Acoustic preference (20%) ---
        likes_acoustic = user_prefs.get("likes_acoustic", False)
        acoustic_score = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]

        # --- Weighted total ---
        total = (
            genre_score   * 0.30 +
            mood_score    * 0.25 +
            energy_score  * 0.25 +
            acoustic_score * 0.20
        )

        # --- Build explanation ---
        reasons = []
        if genre_score == 1.0:
            reasons.append(f"matches your favorite genre ({song['genre']})")
        if mood_score == 1.0:
            reasons.append(f"matches your preferred mood ({song['mood']})")
        if energy_diff < 0.15:
            reasons.append("energy level is close to your target")
        if acoustic_score > 0.7:
            reasons.append("fits your acoustic preference")

        if reasons:
            explanation = "Recommended because it " + " and ".join(reasons)
        else:
            explanation = "Closest available match to your preferences"

        return total, explanation

    scored = [(song, *score_song(song)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
