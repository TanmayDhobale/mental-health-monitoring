from nrclex import NRCLex

def analyze_emotion(text):
    text_object = NRCLex(text)
    return text_object.top_emotions
