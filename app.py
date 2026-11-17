import json, random
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model" / "catbot_model.json"
END = {".", "!", "?"}
PUNCT = {".", "!", "?", ",", ";", ":"}
LABEL = "AI-generated text — this is not a real quote from the speaker."

st.set_page_config(page_title="CATbot", page_icon="🐱", layout="centered")
st.title("🐱 CATbot — Copy-cat Text Generator")
st.caption("A Markov-chain language model that learns word-transition patterns from your transcript dataset.")

@st.cache_resource
def load_model(path, mtime):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    transitions = {}
    for key, value in data["transitions"].items():
        transitions[tuple(key.split("\u241f"))] = value
    return data, transitions

def detokenize(tokens):
    result, cap = [], True
    for tok in tokens:
        if tok in PUNCT:
            if result: result[-1] += tok
            cap = tok in END
        else:
            if cap: tok = tok[:1].upper() + tok[1:]
            result.append(tok); cap = False
    return " ".join(result)

def generate(data, transitions, start, length, order, seed):
    rng = random.Random(seed)
    starts = data["starts"]
    if not starts: raise ValueError("Model has no sentence-start states. Retrain with more transcript text.")
    if start.strip():
        import re
        tokens = re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*|[.!?,;:]", start)
        if len(tokens) >= order:
            out = tokens
            if tuple(t.lower() for t in out[-order:]) not in transitions:
                raise ValueError("That starting phrase was not found in the trained model. Try another phrase or leave it blank.")
        else:
            low = [t.lower() for t in tokens]
            matches = [s for s in starts if [x.lower() for x in s[:len(low)]] == low]
            if not matches: raise ValueError("Starting word not found. Try a different phrase or leave it blank.")
            out = tokens + matches[rng.randrange(len(matches))][len(tokens):]
    else:
        out = list(rng.choice(starts))
    for _ in range(length + 40):
        state = tuple(t.lower() for t in out[-order:])
        choices = transitions.get(state)
        if not choices:
            if len(out) >= length: break
            out += list(rng.choice(starts)); continue
        words, weights = zip(*choices.items())
        out.append(rng.choices(words, weights=weights, k=1)[0])
        if len(out) >= length and out[-1] in END: break
    return out

if not MODEL_PATH.exists():
    st.warning("No trained model found yet. Train in Google Colab, download catbot_model.json, and place it in the project's model folder.")
    st.code(r"CATbot_Complete\model\catbot_model.json")
    st.stop()

data, transitions = load_model(str(MODEL_PATH), MODEL_PATH.stat().st_mtime)
with st.sidebar:
    st.header("Model information")
    st.write(f"**Type:** {data.get('model_type', 'Markov chain')}")
    st.write(f"**Training words:** {data.get('word_count', 0):,}")
    st.write(f"**States:** {len(transitions):,}")
    st.write(f"**Memory order:** {data.get('order', 2)}")
    st.write("**Sources:**")
    for name in data.get("source_files", []): st.caption(name)
    st.divider()
    st.caption("Generated text is synthetic and may be inaccurate or nonsensical.")

st.subheader("Generate text")
with st.form("generate_form"):
    start = st.text_input("Starting phrase (optional)", placeholder="e.g. my dear")
    col1, col2 = st.columns(2)
    with col1: length = st.slider("Output length (tokens)", 30, 300, 100, 10)
    with col2: seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42)
    submitted = st.form_submit_button("Generate CATbot text", type="primary", use_container_width=True)
if submitted:
    try:
        tokens = generate(data, transitions, start, length, data.get("order", 2), int(seed))
        st.markdown("### CATbot response")
        st.write(detokenize(tokens))
        st.info(LABEL)
        st.download_button("Download generated text", detokenize(tokens) + "\n\n" + LABEL, file_name="catbot_output.txt", mime="text/plain")
    except Exception as e:
        st.error(str(e))
