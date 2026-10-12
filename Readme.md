<h2>Artifical Intelligence and Machine Learning</h2>

Copy-cat Bot

A text bot that reads speeches by one person and writes new text in the same style.

Example target: Narendra Modi's speeches (English transcripts). The same idea works for any speaker, such as Obama or a Twitter account.

1. The Idea

If you read enough of a person's speeches, you start to notice patterns:

the words they use again and again
the way they start and end sentences
the phrases that often come together (for example, "my dear friends")

This project teaches a computer to learn those patterns from real speeches, and then use them to produce new text that sounds like the speaker.

The bot does not understand the meaning of what it writes. It only learns which word is likely to come after which words. That is why the output sounds familiar but can be silly or make no sense.

2. What the Bot Does
Input	Output
A large collection of the speaker's speeches	New paragraphs written in the speaker's style
An optional starting word or phrase	Text that continues from that start
3. Data Flow
Speech transcripts (raw text)
        |
        v
[1] Collect data
        |
        v
[2] Clean the text
        |
        v
[3] Split into words (tokens)
        |
        v
[4] Build the model (learn which word follows which)
        |
        v
[5] Generate new text word by word
        |
        v
[6] Check the output
Step 1: Collect data
Get speech transcripts from a public source (for example, a dataset of English transcripts of Modi's speeches).
Save everything as plain .txt files in the data/raw/ folder.
Step 2: Clean the text
Remove web page code (HTML), dates, stage notes like "[applause]", and extra spaces.
Fix text encoding problems.
Save the clean result in data/clean/.
Step 3: Split into words
Break the text into words (tokens). Punctuation is kept or removed depending on how natural we want the output to look.
Step 4: Build the model
Markov chain model (main approach): Go through the text and record, for every group of 2 words, which word came next and how many times.
Example: after "my dear" the next word was "friends" 80 times, "countrymen" 15 times, "brothers" 5 times.
This table of counts is the entire model. No training on a GPU is needed.
Step 5: Generate new text
Pick a starting group of words.
Look up what usually comes next and pick one, using the counts as chances (a word seen more often is picked more often).
Move forward by one word and repeat.
Stop when the text reaches the set length or an end-of-sentence mark.
Step 6: Check the output
Read the output and judge: does it sound like the speaker?
Compare with the real text to make sure the bot is not just copying whole sentences from the speeches.
