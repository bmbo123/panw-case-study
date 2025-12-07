import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

POSITIVE_EMOJIS = {
    "😄", "😃", "😁", "😊", "🙂", "😌", "😍",
    "🤩", "🥳", "🎉", "🔥", "💯", "✨", "❤️", "🤗"
}

NEGATIVE_EMOJIS = {
    "😩", "😭", "😓", "😔", "😢", "😞",
    "😫", "😡", "🤬", "💔", "😤", "💀"
}


def basic_sentiment(text: str) -> float:

    vader_scores = vader.polarity_scores(text)
    return vader_scores["compound"]


def extract_emojis(text: str) -> list:
    return [char for char in text if emoji.is_emoji(char)]


def emoji_sentiment(text: str) -> float:

    score = 0.0
    emoji_count = 0
    
    for char in text:
        if emoji.is_emoji(char):
            emoji_count += 1
            if char in POSITIVE_EMOJIS:
                score += 0.2
            elif char in NEGATIVE_EMOJIS:
                score -= 0.2
    
    if emoji_count > 0:
        return max(-1.0, min(1.0, score))
    return 0.0


def combined_sentiment(text: str) -> float:
    vader_score = basic_sentiment(text)
    emoji_score = emoji_sentiment(text)
    
    combined = vader_score + (emoji_score * 0.3)
    return max(-1.0, min(1.0, combined))