"""Steps 3 and 4: split text into tokens and build the Markov chain model."""
import re
from collections import Counter, defaultdict
from pathlib import Path

# A token is a word (apostrophes/hyphens allowed inside) or one punctuation mark.
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*|[.!?,;:]")
SENTENCE_END = {".", "!", "?"}


def tokenize(text):
    return TOKEN_RE.findall(text)


def load_docs(clean_dir):
    """Return one token list per cleaned file."""
    files = sorted(Path(clean_dir).glob("*.txt"))
    if not files:
        raise SystemExit(f"No cleaned files in {clean_dir}. Run: python src/clean.py")
    return [tokenize(f.read_text(encoding="utf-8")) for f in files]


def build_model(docs, order=2):
    """
    model[(w1, ..., w_order)] = Counter({next_word: times_seen})
    States are lowercase so "My dear" and "my dear" share counts.
    Next words keep their original case so the output looks natural.
    Also returns `starts`: states that began a sentence (repeats = more likely).
    """
    model = defaultdict(Counter)
    starts = []
    for tokens in docs:
        for i in range(len(tokens) - order):
            state = tuple(t.lower() for t in tokens[i:i + order])
            model[state][tokens[i + order]] += 1
            begins_sentence = i == 0 or tokens[i - 1] in SENTENCE_END
            if begins_sentence and state[0] not in SENTENCE_END | {",", ";", ":"}:
                starts.append(state)
    return model, starts


def detokenize(tokens):
    """Turn tokens back into readable text."""
    out, capitalize = [], True
    for tok in tokens:
        if tok in {".", "!", "?", ",", ";", ":"}:
            if out:
                out[-1] += tok
            else:
                out.append(tok)
            capitalize = tok in SENTENCE_END
            continue
        if capitalize:
            tok = tok[:1].upper() + tok[1:]
            capitalize = False
        out.append(tok)
    return " ".join(out)
