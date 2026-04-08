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
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

# Scoring weights — adjust these values to tune the algorithm
GENRE_POINTS = 2.0   # awarded for an exact genre match
MOOD_POINTS  = 1.0   # awarded for an exact mood match
ENERGY_MAX   = 1.0   # maximum points awarded for energy proximity


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against the user's preferences.

    Returns:
        (total_score, reasons) where reasons is a list of strings
        explaining each contribution to the score.
    """
    total   = 0.0
    reasons = []

    # --- Rule 1: Genre match ---
    if song["genre"] == user_prefs.get("genre"):
        total += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")

    # --- Rule 2: Mood match ---
    if song["mood"] == user_prefs.get("mood"):
        total += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    # --- Rule 3: Energy proximity ---
    # The closer the song's energy is to the user's target,
    # the higher the points — smooth gradient, no cliff edges.
    target_energy = user_prefs.get("energy", 0.5)
    energy_diff   = abs(song["energy"] - target_energy)
    energy_points = round(ENERGY_MAX * (1.0 - energy_diff), 2)
    total        += energy_points
    reasons.append(f"energy close to target (+{energy_points})")

    return round(total, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Scores every song, ranks by score descending, returns top k.
    """
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
