# PANW-CASE-STUDY AI JOURNAL

## Challenge

The case study wants you to build a tool that reads journal entries and figures out the person's mood and energy. But it's not just about matching keywords. The tricky part is that the same word can mean totally different things depending on context.

Like "I'm crushing it at work" is good. But "The workload is crushing me" is bad. Both have "crushing" in them but one is positive and one is negative. A dumb keyword filter would break on this.

PANW specifically calls this out as the test of whether you can actually write logic that understands language vs just counting words. They also want you to use existing libraries instead of building everything from scratch.

## Implementation

I built it three parts. First, I check if the text has specific patterns that matter. Like with "crushing", I parse the sentence to see if the object is "it" (positive) or "me" (negative). That handles the ambiguous case right away.

Then I check for emojis. If there are a bunch of negative emojis, that's a strong signal so I weight it heavily.

Then I fall back to VADER, which is a pre-made sentiment analyzer. You give it text and it returns a score between -1 and 1 telling you how negative or positive it is. It handles negation and intensifiers automatically. I set the threshold so anything above 0.1 is positive and below -0.1 is negative.

That's it. Context check first, emojis second, then the sentiment score.

### Testing

For testing, I had some phrases that I knew the verbage and tone for and tested it against our analyzer. Things like "I'm crushing it at work" should be positive, "the workload is crushing me" should be negative, "not happy" should flip to negative even though happy is positive. I covered the obvious cases plus edge cases like empty strings, emoji-only entries, mixed case sensitivity, and making sure entries actually save to storage.

20 tests total, all pass.

## What I Could Add / Do Better

1. **Web Frontend**: Right now it's command line only. A web app would be way better. Users could type entries in a text box, see the mood prediction show up, look at their history and charts showing mood over time. Could show trends, filter by emotion, all that stuff.

2. **More Nuanced Emotion Output**: Currently it's just "positive/negative/neutral". Could expand to specific emotions like anger, sadness, anxiety, joy, stress, excitement, etc. That would tell users more about what they're actually feeling instead of just good or bad.

3. **Better Emoji Handling**: I tried using a big dataset of emoji sentiments at first but it was garbage. The mappings were weird, like certain emojis werent accurately represented in their real world usages. So I switched to just manually picking the common journaling emojis. For a real version I'd expand the list but keep it curated, not automated.

4. **Batch Processing**: Right now you add one entry at a time. Could load a CSV of old journal entries and analyze them all at once. Would be useful if someone wanted to import their existing journal.

5. **Export Functionality**: Save the results to CSV or PDF. Generate reports like "you were positive 70% of the time this week" with breakdowns by emotion.

6. **Negation Refinement**: VADER handles some negation but not all of it. Could add explicit rules for common patterns like "I'm not feeling good" vs "I'm not feeling bad" which are pretty different.

7. **Contextual Rule Expansion**: Only "crush" gets special handling right now. Could add rules for other ambiguous words like "killing it", "dying", "overwhelmed", etc. Same pattern matching approach.

For the case study the lean approach works fine. But for a real app you'd want the web interface, better emotion stuff, and more contextual rules.

#### USE of AI DISCLOSURE

I used ChatGPT/Claude to research NLP libraries and figure out which ones would be good for this. It explained how spaCy's dependency parsing works and what VADER does. I didn't know much about either of those going in so that was helpful. It also explained some basic linguistics stuff about how sentences are structured.
I also used GitHub Copilot while writing the code. It helped me write boilerplate and some of the helper functions. But I reviewed everything it generated and modified stuff when it wasn't right. The overall architecture and the contextual logic (checking for "crush" patterns, emoji handling, how everything flows together) was mainly done by me.
I tested everything myself and fixed bugs.
Using these tools really allowed me to deliver a solution really fast for the hackathon.
