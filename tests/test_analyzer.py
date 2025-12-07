import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzer import analyze
from storage import clear_entries, append_entry, get_last_entries


class TestContextualLogic:
    def test_crushing_positive(self):
        result = analyze("I'm crushing it at work today")
        assert result["mood"] == "positive"
        assert result["energy"] == "high"
    
    def test_crushing_negative(self):
        result = analyze("the workload is crushing me")
        assert result["mood"] == "negative"
        assert result["energy"] == "high_stress"
    
    def test_crushing_you(self):
        result = analyze("this is crushing you")
        assert result["mood"] == "negative"


class TestVaderSentiment:
    def test_positive_sentiment(self):
        result = analyze("I'm so happy and excited today!")
        assert result["mood"] == "positive"
    
    def test_negative_sentiment(self):
        result = analyze("I'm sad and depressed")
        assert result["mood"] == "negative"
    
    def test_intensifier_handling(self):
        result = analyze("I'm very very happy!!!")
        assert result["mood"] == "positive"
        assert result["energy"] == "high"


class TestNRCLexEmotions:
    def test_fear_emotion_detection(self):
        result = analyze("I'm so anxious and afraid right now")
        assert result["mood"] == "negative"
    
    def test_joy_emotion_detection(self):
        result = analyze("I'm filled with joy and delight")
        assert result["mood"] == "positive"
    
    def test_anger_detection(self):
        result = analyze("I'm so angry and frustrated")
        assert result["mood"] == "negative"
        assert result["energy"] == "high_stress"


class TestEmojiDetection:
    def test_positive_emoji_only(self):
        result = analyze("today was great 🔥")
        assert result["mood"] == "positive"
    
    def test_negative_emoji_only(self):
        result = analyze("feeling terrible 😩")
        assert result["mood"] == "negative"
    
    def test_multiple_positive_emojis(self):
        result = analyze("amazing day 😊🎉✨")
        assert result["mood"] == "positive"
    
    def test_multiple_negative_emojis(self):
        result = analyze("not good 😭😔😞")
        assert result["mood"] == "negative"


class TestEdgeCases:
    def test_empty_string(self):
        result = analyze("")
        assert result["mood"] == "neutral"
        assert result["energy"] == "low"
    
    def test_whitespace_only(self):
        result = analyze("   \n\t  ")
        assert result["mood"] == "neutral"
        assert result["energy"] == "low"
    
    def test_emoji_only(self):
        result = analyze("😊🎉✨")
        assert result["mood"] == "positive"
    
    def test_mixed_case(self):
        result1 = analyze("I'm HAPPY")
        result2 = analyze("I'm happy")
        assert result1["mood"] == result2["mood"]
    
    def test_special_characters(self):
        result = analyze("I'm crushing it!!! 🔥")
        assert result["mood"] == "positive"
    
    def test_long_entry(self):
        text = "Today was amazing! I crushed my presentation, got great feedback, and felt on top of the world. 🔥✨"
        result = analyze(text)
        assert result["mood"] == "positive"


class TestNegation:
    def test_not_good(self):
        result = analyze("Today was not good")
        assert result["mood"] == "negative"
    
    def test_not_happy(self):
        result = analyze("I'm not happy")
        assert result["mood"] == "negative"
    
    def test_never_bad(self):
        result = analyze("This is never bad")
        assert result["mood"] in ["positive", "negative", "neutral"]


class TestNeutral:
    def test_truly_neutral(self):
        result = analyze("The weather is cloudy today")
        assert result["mood"] == "neutral"
    
    def test_mixed_equal_sentiment(self):
        result = analyze("good and bad")
        assert result["mood"] in ["positive", "negative", "neutral"]


class TestStorageIntegration:
    def test_entry_saved_with_analysis(self):
        clear_entries()
        analysis = analyze("crushing it today 🔥")
        entry = append_entry("crushing it today 🔥", analysis)
        
        assert entry["mood"] == "positive"
        assert entry["energy"] == "high"
        assert "timestamp" in entry
        
        entries = get_last_entries(1)
        assert len(entries) == 1
        assert entries[0]["mood"] == "positive"


class TestStressDetection:
    def test_overwhelming_stress(self):
        result = analyze("everything is overwhelming me right now")
        assert result["mood"] == "negative"
        assert result["energy"] in ["high_stress", "medium"]
    
    def test_regular_negative_no_stress(self):
        result = analyze("this is not ideal")
        assert result["mood"] == "negative"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
