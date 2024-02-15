from nrclex import NRCLex

def analyze_emotion(text):
    text_object = NRCLex(text)
    emotions = text_object.affect_frequencies
    sentiment = 'Positive' if emotions['positive'] > emotions['negative'] else 'Negative' if emotions['negative'] > emotions['positive'] else 'Neutral'
    top_emotion = text_object.top_emotions[0][0] if text_object.top_emotions else None
    
    return emotions, sentiment, top_emotion
