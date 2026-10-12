# Copy-cat Bot

A text bot that reads speeches by one person and writes new text in the same style.

Example target: **Narendra Modi's speeches** (English transcripts). The same idea works for any speaker, such as Obama or a Twitter account.

---

## 1. The Idea

If you read enough of a person's speeches, you start to notice patterns:

- the words they use again and again
- the way they start and end sentences
- the phrases that often come together (for example, "my dear friends")

This project teaches a computer to learn those patterns from real speeches, and then use them to produce **new** text that sounds like the speaker.

The bot does not understand the meaning of what it writes. It only learns **which word is likely to come after which words**. That is why the output sounds familiar but can be silly or make no sense.

---

## 2. What the Bot Does

| Input | Output |
|-------|--------|
| A large collection of the speaker's speeches | New paragraphs written in the speaker's style |
| An optional starting word or phrase | Text that continues from that start |

---

## 3. Data Flow

```
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
```

### Step 1: Collect data
- Get speech transcripts from a public source (for example, a dataset of English transcripts of Modi's speeches).
- Save everything as plain `.txt` files in the `data/raw/` folder.

### Step 2: Clean the text
- Remove web page code (HTML), dates, stage notes like "[applause]", and extra spaces.
- Fix text encoding problems.
- Save the clean result in `data/clean/`.

### Step 3: Split into words
- Break the text into words (tokens). Punctuation is kept or removed depending on how natural we want the output to look.

### Step 4: Build the model
- **Markov chain model (main approach):** Go through the text and record, for every group of 2 words, which word came next and how many times.
  - Example: after "my dear" the next word was "friends" 80 times, "countrymen" 15 times, "brothers" 5 times.
- This table of counts is the entire model. No training on a GPU is needed.

### Step 5: Generate new text
1. Pick a starting group of words.
2. Look up what usually comes next and pick one, using the counts as chances (a word seen more often is picked more often).
3. Move forward by one word and repeat.
4. Stop when the text reaches the set length or an end-of-sentence mark.

### Step 6: Check the output
- Read the output and judge: does it sound like the speaker?
- Compare with the real text to make sure the bot is **not just copying whole sentences** from the speeches.

---

## 4. Project Structure

```
copycat-bot/
|-- data/
|   |-- raw/          # original transcripts
|   |-- clean/        # cleaned text
|-- src/
|   |-- clean.py      # step 2
|   |-- model.py      # steps 3 and 4
|   |-- generate.py   # step 5
|-- README.md
|-- requirements.txt
```

---

## 5. How to Run

```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Clean the data
python src/clean.py

# 3. Build the model and generate text
python src/generate.py --start "my dear" --length 100
```

---

## 6. Example Output

> _Add a real output from your own bot here after you run it._

Do not write an example by hand. Your teacher will want to see what the bot really produced, including its mistakes.

---

## 7. Limitations

- **It does not understand meaning.** The text may look correct but say nothing useful.
- **It needs a lot of data.** With only a few speeches, the bot will repeat the original sentences almost word for word. A good target is tens of thousands of words or more.
- **It only looks at the last 1-3 words.** It forgets what it said earlier, so long paragraphs may drift off topic.
- **It copies the speaker's style, not their opinions.** The output must never be treated as something the person actually said.

---

## 8. Responsible Use

This bot makes text that **sounds like a real person but was not written by them**. It is for learning only.

- Label all generated text as "AI-generated".
- Do not post it as real quotes from the speaker.

---

## 9. Possible Improvements

- Use a bigger group of words (3-word memory) and compare the results.
- Replace the Markov model with a small neural network (LSTM) and compare quality.
- Measure how close the output is to real text, not only by reading it.
- Try the same bot on a different speaker and compare.

---

## 10. Tools Used

- Python 3
- Standard libraries for text handling (`re`, `random`, `collections`)
- Optional: `nltk` for splitting text into sentences
