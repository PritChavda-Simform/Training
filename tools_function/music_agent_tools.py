from langchain_core.tools import tool
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from dummy_data.music_agent_dummy_data import mood_genre_map,genre_songs

@tool
def mood_to_genre(mood: str) -> str:
    """
        Maps a user's emotional mood to an appropriate music genre. This function is useful for mood-based music recommendations.
    """

    mood = mood.lower()
    return mood_genre_map.get(mood, "pop")
@tool
def fetch_song(genre: str) -> str:
    """
        Fetches a random song recommendation from a given music genre. Ideal for quick suggestions or surprises based on genre preferences.
    """
 
    return random.choice(genre_songs.get(genre, ["No songs found."]))
@tool
def fetch_playlist(genre: str) -> str:
    """
       Generates a formatted playlist of songs for a given genre. Useful for creating genre-specific listening sessions.
    """

    songs = genre_songs.get(genre, ["No playlist found."])
    return f"Here's your {genre.title()} playlist:\n" + "\n".join(f"- {song}" for song in songs)
