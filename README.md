# CATbot — Complete local + Google Colab version

CATbot learns word-transition patterns from text transcripts and generates new text in a similar style. The main model is a **word-level Markov chain**. It is lightweight and runs on CPU; Google Colab GPU is optional only for the notebook's experimental LSTM section.

> Generated text is synthetic. Do not present it as a real quote from the speaker.

## Project files

- `copycat_bot_colab.ipynb` — Colab notebook; includes a final export cell to download `catbot_model.json`.
- `clean.py`, `model.py`, `generate.py` — original project pipeline.
- `train_export.py` — local alternative: clean raw transcripts, train Markov chain and export JSON.
- `app.py` — Streamlit web interface for the trained model.
- `model/` — put the downloaded `catbot_model.json` here.
- `data/raw/` — add your source `.txt` transcripts here.

## A. Train in Google Colab (recommended for your lab demo)

1. Open https://colab.research.google.com/
2. Choose **File → Upload notebook**, then upload `copycat_bot_colab.ipynb`.
3. Put your `.txt` transcript files in Google Drive at `MyDrive/copycat-bot/raw`, OR change `DATA_SOURCE = "upload"` in the notebook and upload files when prompted.
4. Run cells from top to bottom. The main Markov model does not need a GPU. The optional LSTM part can be skipped.
5. Run the final **Export the trained model** cell. It downloads `catbot_model.json`.
6. Copy that file into this project's `model` folder. The final path must be `CATbot_Complete/model/catbot_model.json`.

**Dataset:** use multiple substantial plain-text transcripts from the same speaker. The notebook's example uses English speeches. Aim for 20,000+ words; a larger clean dataset generally gives better variety. Use data you are permitted to use.

## B. Run on Windows laptop

Open PowerShell in the extracted `CATbot_Complete` folder (the folder containing `app.py`) and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, run this once in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in Chrome. You can also double-click `run_catbot.bat` after installing dependencies.

## C. If you want to train locally instead

Put `.txt` transcripts in `data/raw/`, then run:

```powershell
python train_export.py
python -m streamlit run app.py
```

## Suggested lab demonstration

1. Show the transcript dataset and explain why text cleaning is needed.
2. Explain tokenization and Markov states: with order 2, the model uses the previous two tokens to predict the next token.
3. Show the training statistics in the app sidebar (words, states, model order).
4. Enter a starting phrase found in your dataset, or leave it blank for a random start.
5. Generate output twice with different random seeds.
6. Explain limitations: no semantic understanding; output can be repetitive or nonsensical.

## Important technical note

The project's primary Markov model is not neural-network gradient training. It learns transition frequencies from the transcript corpus, so it does not require a GPU. The notebook's LSTM is a separate optional experiment. The portable JSON export added to the notebook is for the Markov model used by the local Streamlit app.
