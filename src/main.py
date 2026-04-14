"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


# Define distinct user preference profiles for testing
USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    "Peaceful Acoustic": {
        "genre": "folk",
        "mood": "peaceful",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    # Edge case: Conflicting preferences
    "Contradictory Mix": {
        "genre": "electronic",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}\n")
    
    # Test each profile
    for profile_name, user_prefs in USER_PROFILES.items():
        print("=" * 70)
        print(f"PROFILE: {profile_name}")
        print(f"Preferences: {user_prefs}")
        print("=" * 70)
        
        recommendations = recommend_songs(user_prefs, songs, k=5)
        
        print("\nTop 5 recommendations:\n")
        for rank, rec in enumerate(recommendations, 1):
            song, score, reasons = rec
            print(f"{rank}. Title: {song['title']} by {song['artist']}")
            print(f"   Genre: {song['genre']}, Mood: {song['mood']}, Energy: {song['energy']}")
            print(f"   Score: {score:.2f}")
            print(f"   Reasons: {', '.join(reasons)}")
            print()


if __name__ == "__main__":
    main()
