from textblob import TextBlob

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns polarity (-1 to 1)

def test_get_sentiment():
    positive_text = "I am very happy today!"
    negative_text = "I am very sad today."
    
    positive_score = get_sentiment(positive_text)
    negative_score = get_sentiment(negative_text)
    
    print(f"Positive score: {positive_score}, Expected: > 0")
    print(f"Negative score: {negative_score}, Expected: < 0")

test_get_sentiment()
from textblob import TextBlob

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns polarity (-1 to 1)

def test_get_sentiment():
    positive_text = "I am very happy today!"
    negative_text = "I am very sad today."
    
    positive_score = get_sentiment(positive_text)
    negative_score = get_sentiment(negative_text)
    
    print(f"Positive score: {positive_score}, Expected: > 0")
    print(f"Negative score: {negative_score}, Expected: < 0")

test_get_sentiment()
