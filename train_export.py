"""Clean transcripts, train the Markov model and export it as JSON."""
import json
from pathlib import Path
from clean import clean_text, read_text
from model import tokenize, build_model

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "model" / "catbot_model.json"
ORDER = 2

def main():
    files = sorted(RAW.glob("*.txt"))
    files = [p for p in files if p.name != "PUT_TRANSCRIPTS_HERE.txt"]
    if not files:
        raise SystemExit("No transcript .txt files found in data/raw. Add at least one transcript first.")
    CLEAN.mkdir(parents=True, exist_ok=True)
    docs = []
    total_words = 0
    for path in files:
        cleaned = clean_text(read_text(path))
        (CLEAN / path.name).write_text(cleaned, encoding="utf-8")
        tokens = tokenize(cleaned)
        if len(tokens) > ORDER:
            docs.append(tokens)
        total_words += len(cleaned.split())
    if not docs:
        raise SystemExit("Transcript files contain too little usable text.")
    transitions, starts = build_model(docs, ORDER)
    payload = {
        "format_version": 1,
        "model_type": "word-level Markov chain",
        "order": ORDER,
        "source_files": [p.name for p in files],
        "word_count": total_words,
        "token_count": sum(map(len, docs)),
        "transitions": {"\u241f".join(state): dict(counts) for state, counts in transitions.items()},
        "starts": [list(s) for s in starts]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Trained Markov model from {len(files)} transcript(s)")
    print(f"Words: {total_words:,} | Tokens: {payload['token_count']:,} | States: {len(transitions):,}")
    print(f"Saved model: {OUT}")
    if total_words < 20000:
        print("WARNING: Dataset is small; output may repeat training text. Add more transcripts if possible.")

if __name__ == "__main__":
    main()
