"""Step 2: clean raw transcripts in data/raw/ and save to data/clean/."""
import argparse
import html
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STAGE_WORDS = (r"applause|laughter|laughs|cheers|cheering|music|audience|interruption|"
               r"inaudible|pause|crosstalk|slogans|video|chanting|clapping|translation")
RE_TAGS = re.compile(r"<[^>]+>")
RE_URLS = re.compile(r"https?://\S+|www\.\S+")
RE_SQUARE = re.compile(r"\[[^\]]{0,100}\]")                       # [applause], [inaudible]
RE_PAREN_STAGE = re.compile(rf"\((?=[^)]*(?:{STAGE_WORDS}))[^)]{{0,100}}\)", re.I)
MONTHS = r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
RE_DATES = re.compile(
    rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+{MONTHS}\.?,?\s+\d{{4}}\b"   # 12 March 2019
    rf"|\b{MONTHS}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b"  # March 12, 2019
    r"|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"                         # 12/03/2019
    r"|\b\d{4}-\d{2}-\d{2}\b",                                    # 2019-03-12
    re.I,
)
QUOTES = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
          "\u2013": "-", "\u2014": " - ", "\u2026": "..."}


def read_text(path: Path) -> str:
    """Fix encoding problems: try UTF-8 first, then Windows-1252, then Latin-1."""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = RE_TAGS.sub(" ", text)
    text = unicodedata.normalize("NFKC", text)
    for bad, good in QUOTES.items():
        text = text.replace(bad, good)
    text = RE_URLS.sub(" ", text)
    text = RE_SQUARE.sub(" ", text)
    text = RE_PAREN_STAGE.sub(" ", text)
    text = RE_DATES.sub(" ", text)
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")
    return re.sub(r"\s+", " ", text).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", default=ROOT / "data" / "raw")
    ap.add_argument("--out", default=ROOT / "data" / "clean")
    args = ap.parse_args()

    raw_dir, out_dir = Path(args.raw), Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(raw_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files found in {raw_dir}. Put the raw transcripts there first.")

    total = 0
    for f in files:
        cleaned = clean_text(read_text(f))
        (out_dir / f.name).write_text(cleaned, encoding="utf-8")
        total += len(cleaned.split())
    print(f"Cleaned {len(files)} file(s), about {total:,} words -> {out_dir}")
    if total < 20_000:
        print("WARNING: under ~20,000 words. The bot will mostly repeat the originals.")


if __name__ == "__main__":
    main()
