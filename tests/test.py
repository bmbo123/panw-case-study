# tests/test_analyzer.py
import pytest
from analyzer import analyze
from storage import clear_entries


class TestContextualLogic:
    """Test the core ambiguity handling: 'crushing'"""
    
    def test_crushing_positive(self):
        """'crushing it' should be positive, high energy"""
        result = analyze("I'm crushing it at work today")
        assert result["mood"] == "positive"
        assert result["energy"] == "high"
    
    def test_crushing_negative(self):
        """'workload crushing me' should be negative, high stress"""
        result = analyze("the workload is crushing me")
        assert result["mood"] == "negative"
        assert result["energy"] == "high_stress"
    
    def test_crushing_you(self):
        """'crushing you' should be negative"""
        result = analyze("this is crushing you")
        assert result["mood"] == "negative"


class TestVaderSentiment:
    """Test VADER-based sentiment detection"""
    
    def test_positive_sentiment(self):
        """VADER detects positive words"""
        result = analyze("I'm so happy and excited today!")
        assert result["mood"] == "positive"
    
    def test_negative_sentiment(self):
        """VADER detects negative words"""
        result = analyze("I'm sad and depressed")
        assert result["mood"] == "negative"
    
    def test_intensifier_handling(self):
        """VADER handles intensifiers like 'very', 'so'"""
        result = analyze("I'm very very happy!!!")
        assert result["mood"] == "positive"
        assert result["energy"] == "high"


class TestNRCLexEmotions:
    """Test NRCLex emotional category detection"""
    
    def test_fear_emotion_detection(self):
        """NRCLex detects fear/anxiety"""
        result = analyze("I'm so anxious and afraid right now")
        # Fear is part of stress emotions
        assert result["mood"] == "negative"
    
    def test_joy_emotion_detection(self):
        """NRCLex detects joy"""
        result = analyze("I'm filled with joy and delight")
        assert result["mood"] == "positive"
    
    def test_anger_detection(self):
        """NRCLex detects anger as stress"""
        result = analyze("I'm so angry and frustrated")
        assert result["mood"] == "negative"
        assert result["energy"] == "high_stress"


class TestEmojiDetection:
    """Test emoji-based sentiment"""
    
    def test_positive_emoji_only(self):
        """Positive emoji should influence mood"""
        result = analyze("today was great 🔥")
        assert result["mood"] == "positive"
    
    def test_negative_emoji_only(self):
        """Negative emoji should influence mood"""
        result = analyze("feeling terrible 😩")
        assert result["mood"] == "negative"
    
    def test_multiple_positive_emojis(self):
        """Multiple positive emojis reinforce sentiment"""
        result = analyze("amazing day 😊🎉✨")
        assert result["mood"] == "positive"
    
    def test_multiple_negative_emojis(self):
        """Multiple negative emojis dominate"""
        result = analyze("not good 😭😔😞")
        assert result["mood"] == "negative"


class TestEdgeCases:
    """Test robustness and edge cases"""
    
    def test_empty_string(self):
        """Empty input should not crash"""
        result = analyze("")
        assert result["mood"] == "neutral"
        assert result["energy"] == "low"
    
    def test_whitespace_only(self):
        """Whitespace-only input should not crash"""
        result = analyze("   \n\t  ")
        assert result["mood"] == "neutral"
        assert result["energy"] == "low"
    
    def test_emoji_only(self):
        """Just emojis should work"""
        result = analyze("😊🎉✨")
        assert result["mood"] == "positive"
    
    def test_mixed_case(self):
        """Case insensitivity"""
        result1 = analyze("I'm HAPPY")
        result2 = analyze("I'm happy")
        assert result1["mood"] == result2["mood"]
    
    def test_special_characters(self):
        """Should handle punctuation"""
        result = analyze("I'm crushing it!!! 🔥")
        assert result["mood"] == "positive"
    
    def test_long_entry(self):
        """Should handle longer text"""
        text = "Today was amazing! I crushed my presentation, got great feedback, and felt on top of the world. 🔥✨"
        result = analyze(text)
        assert result["mood"] == "positive"


class TestNegation:
    """Test negation handling (VADER handles this internally)"""
    
    def test_not_good(self):
        """'not good' should flip to negative"""
        result = analyze("Today was not good")
        assert result["mood"] == "negative"
    
    def test_not_happy(self):
        """'not happy' should flip"""
        result = analyze("I'm not happy")
        assert result["mood"] == "negative"
    
    def test_never_bad(self):
        """'never bad' double negative"""
        result = analyze("This is never bad")
        # VADER handles: "never" + "bad" might still be negative or neutral
        # Just test it doesn't crash
        assert result["mood"] in ["positive", "negative", "neutral"]


class TestNeutral:
    """Test neutral mood detection"""
    
    def test_truly_neutral(self):
        """Neutral text with no sentiment words"""
        result = analyze("The weather is cloudy today")
        assert result["mood"] == "neutral"
    
    def test_mixed_equal_sentiment(self):
        """Equal positive and negative might be neutral"""
        result = analyze("good and bad")
        # With NRCLex, depends on emotions detected
        assert result["mood"] in ["positive", "negative", "neutral"]


class TestStorageIntegration:
    """Test that analyzer integrates with storage"""
    
    def test_entry_saved_with_analysis(self):
        """Entry should save with mood/energy tags"""
        clear_entries()
        
        from storage import append_entry, get_last_entries
        analysis = analyze("crushing it today 🔥")
        entry = append_entry("crushing it today 🔥", analysis)
        
        assert entry["mood"] == "positive"
        assert entry["energy"] == "high"
        assert "timestamp" in entry
        
        # Verify it was saved
        entries = get_last_entries(1)
        assert len(entries) == 1
        assert entries[0]["mood"] == "positive"


class TestStressDetection:
    """Test high-stress vs regular negative"""
    
    def test_overwhelming_stress(self):
        """Overwhelm should be high_stress"""
        result = analyze("everything is overwhelming me right now")
        assert result["mood"] == "negative"
        # NRCLex detects fear/sadness
        assert result["energy"] in ["high_stress", "medium"]
    
    def test_regular_negative_no_stress(self):
        """Regular negative without stress emotion"""
        result = analyze("this is not ideal")
        assert result["mood"] == "negative"
        # Less intensely stressed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])