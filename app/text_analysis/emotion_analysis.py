from nrclex import NRCLex
from collections import Counter

def analyze_emotion(text):
    try:
        print(f"Analyzing emotion for: '{text}'")
        text_object = NRCLex(text)
        emotion_frequencies = text_object.affect_frequencies
        print(f"Emotion frequencies: {emotion_frequencies}")

        # Check if emotion frequencies are empty or not detected
        if not emotion_frequencies or all(value == 0 for value in emotion_frequencies.values()):
            print("Warning: No emotions detected. This may be due to the text content or NRCLex limitations.")
        return emotion_frequencies
    except Exception as e:
        print(f"Error analyzing emotion: {e}")
        return {}