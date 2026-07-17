"""
Phishing Email Detection System — Streamlit GUI
================================================
Features:
  • Paste email text OR upload a .eml / .txt file
  • AI model classifies it as SAFE or PHISHING
  • Safe emails are hashed (SHA-256) and stored on Ganache blockchain
  • Full blockchain history viewer
  • Confidence score + per-label probability bars

Run:
    streamlit run app.py

Requirements (besides your ML artifacts):
    pip install streamlit web3 py-solc-x python-dotenv
"""

import os
import json
import time
import pickle
import hashlib
import warnings
from pathlib import Path
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser

import numpy as np
import streamlit as st
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
ARTIFACT_DIR    = Path("artifacts")
DEPLOYMENT_JSON = Path("EmailRegistry_Deployment.json")
GANACHE_URL     = os.getenv("GANACHE_URL",          "http://127.0.0.1:7545")
ACCOUNT_ADDRESS = os.getenv("GANACHE_ACCOUNT",      "")
PRIVATE_KEY     = os.getenv("GANACHE_PRIVATE_KEY",  "")
LSTM_MAX_LEN    = 150

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CrypPhish AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
}

/* Cards */
.card {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.card-safe {
    background: linear-gradient(135deg, #052e16 0%, #111827 100%);
    border: 1px solid #166534;
}

.card-phishing {
    background: linear-gradient(135deg, #2d0a0a 0%, #111827 100%);
    border: 1px solid #7f1d1d;
}

/* Result badge */
.badge-safe {
    display: inline-block;
    background: #166534;
    color: #bbf7d0;
    padding: 0.4rem 1.2rem;
    border-radius: 99px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
}

.badge-phishing {
    display: inline-block;
    background: #7f1d1d;
    color: #fecaca;
    padding: 0.4rem 1.2rem;
    border-radius: 99px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
}

/* Hash display */
.hash-box {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    background: #0a0e1a;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    word-break: break-all;
    color: #60a5fa;
    line-height: 1.6;
}

/* Tx hash */
.tx-box {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    background: #0a0e1a;
    border: 1px solid #2d4a1e;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    word-break: break-all;
    color: #86efac;
}

/* Section headers */
h1 { font-family: 'DM Sans', sans-serif; font-weight: 700; color: #f1f5f9; }
h2 { font-family: 'DM Sans', sans-serif; font-weight: 600; color: #cbd5e1; }
h3 { color: #94a3b8; font-weight: 400; }

/* Override streamlit buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37,99,235,0.4);
}

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
.metric-card {
    flex: 1;
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    color: #60a5fa;
}
.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
}

/* History table */
.history-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    background: #111827;
    border: 1px solid #1e2d4a;
    font-size: 0.85rem;
}

/* Divider */
hr { border-color: #1e2d4a; }

/* Progress bar label */
.prob-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 0.2rem;
}

/* Info / warning boxes */
.info-box {
    background: #0c1a2e;
    border-left: 3px solid #3b82f6;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.85rem;
    color: #93c5fd;
    margin-bottom: 1rem;
}
.warn-box {
    background: #1c0a0a;
    border-left: 3px solid #ef4444;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.85rem;
    color: #fca5a5;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# LOAD ML ARTIFACTS  (cached so they load only once)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_ml_artifacts():
    """Load vectorizer + best model + label mapping."""
    vec_path    = ARTIFACT_DIR / "tfidf_vectorizer.pkl"
    lm_path     = ARTIFACT_DIR / "label_mapping.json"
    best_txt    = ARTIFACT_DIR / "best_model.txt"

    errors = []
    for p in [vec_path, lm_path, best_txt]:
        if not p.exists():
            errors.append(str(p))
    if errors:
        return None, None, None, None, f"Missing artifact files:\n" + "\n".join(errors)

    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(lm_path) as f:
        lm = json.load(f)

    int_to_label = {int(k): v for k, v in lm["int_to_label"].items()}
    best_info    = open(best_txt).read()
    is_lstm      = "best_model.keras" in best_info

    if is_lstm:
        import tensorflow as tf
        from tensorflow.keras.preprocessing.text import tokenizer_from_json
        model = tf.keras.models.load_model(ARTIFACT_DIR / "best_model.keras")
        with open(ARTIFACT_DIR / "lstm_tokenizer.json") as f:
            lstm_tok = tokenizer_from_json(f.read())
        return model, vectorizer, int_to_label, lstm_tok, None
    else:
        model_path = ARTIFACT_DIR / "best_model.pkl"
        if not model_path.exists():
            return None, None, None, None, f"Missing {model_path}"
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model, vectorizer, int_to_label, None, None


# ──────────────────────────────────────────────────────────────────────────────
# BLOCKCHAIN  (cached connection)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_blockchain():
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        if not w3.is_connected():
            return None, None, "Cannot connect to Ganache. Make sure it is running on port 7545."
        if not DEPLOYMENT_JSON.exists():
            return w3, None, "EmailRegistry_Deployment.json not found. Deploy the contract first (Cell 10 in your notebook)."
        with open(DEPLOYMENT_JSON) as f:
            dep = json.load(f)
        contract = w3.eth.contract(address=dep["address"], abi=dep["abi"])
        return w3, contract, None
    except ImportError:
        return None, None, "web3 not installed. Run: pip install web3"
    except Exception as e:
        return None, None, str(e)


# ──────────────────────────────────────────────────────────────────────────────
# PREPROCESSING  (mirrors your notebook)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_nlp():
    import nltk
    for r in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
        nltk.download(r, quiet=True)
    from nltk.corpus import stopwords
    from nltk.stem   import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    return set(stopwords.words("english")), WordNetLemmatizer(), word_tokenize

def preprocess(text: str, stop_words, lemmatizer, word_tokenize) -> str:
    tokens = word_tokenize(str(text))
    tokens = [lemmatizer.lemmatize(w.lower())
               for w in tokens
               if w.isalpha() and w.lower() not in stop_words]
    return " ".join(tokens)


# ──────────────────────────────────────────────────────────────────────────────
# PREDICTION
# ──────────────────────────────────────────────────────────────────────────────
def predict(raw_text: str):
    """Returns (label_str, confidence_float, probabilities_dict)."""
    model, vec, int_to_label, lstm_tok, err = load_ml_artifacts()
    if err:
        return None, None, None, err

    stop_words, lemmatizer, word_tokenize = load_nlp()
    processed = preprocess(raw_text, stop_words, lemmatizer, word_tokenize)

    if lstm_tok is not None:                      # LSTM branch
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        seq   = lstm_tok.texts_to_sequences([processed])
        X     = pad_sequences(seq, maxlen=LSTM_MAX_LEN, padding="post", truncating="post")
        proba = model.predict(X, verbose=0)[0]
        idx   = int(np.argmax(proba))
        label = int_to_label[idx]
        probs = {int_to_label[i]: float(p) for i, p in enumerate(proba)}
    else:                                          # sklearn branch
        X     = vec.transform([processed])
        idx   = int(model.predict(X)[0])
        label = int_to_label[idx]
        proba = model.predict_proba(X)[0] if hasattr(model, "predict_proba") else None
        if proba is not None:
            probs = {int_to_label[i]: float(p) for i, p in enumerate(proba)}
        else:
            probs = {label: 1.0}

    confidence = probs.get(label, 1.0)
    return label, confidence, probs, None


# ──────────────────────────────────────────────────────────────────────────────
# BLOCKCHAIN HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def store_on_blockchain(email_hash: str, sender: str, subject: str, prediction: str):
    w3, contract, err = load_blockchain()
    if err:
        return None, err
    if not ACCOUNT_ADDRESS or not PRIVATE_KEY:
        return None, "GANACHE_ACCOUNT / GANACHE_PRIVATE_KEY not set in .env"
    try:
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn   = contract.functions.storeEmail(
            email_hash, sender, subject, prediction
        ).build_transaction({
            "from":      ACCOUNT_ADDRESS,
            "nonce":     nonce,
            "gas":       3_000_000,
            "gasPrice":  w3.to_wei("20", "gwei"),
        })
        signed  = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        raw     = getattr(signed, "rawTransaction",
                  getattr(signed, "raw_transaction", None))
        tx_hash = w3.eth.send_raw_transaction(raw)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex(), None
    except Exception as e:
        return None, str(e)


def fetch_blockchain_history():
    w3, contract, err = load_blockchain()
    if err:
        return [], err
    try:
        total   = contract.functions.getEmailCount().call()
        records = []
        for i in range(total):
            h, sender, subject, pred, ts = contract.functions.getEmail(i).call()
            records.append({
                "id":         i,
                "hash":       h,
                "sender":     sender,
                "subject":    subject,
                "prediction": pred,
                "timestamp":  datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            })
        return list(reversed(records)), None   # newest first
    except Exception as e:
        return [], str(e)


# ──────────────────────────────────────────────────────────────────────────────
# EMAIL PARSER
# ──────────────────────────────────────────────────────────────────────────────
def parse_eml_bytes(raw_bytes: bytes) -> dict:
    msg     = BytesParser(policy=policy.default).parsebytes(raw_bytes)
    sender  = str(msg["From"]    or "unknown")
    subject = str(msg["Subject"] or "No Subject")
    body    = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")
    return {"sender": sender, "subject": subject, "body": body}


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ CrypPhish AI")
    st.markdown("<hr style='border-color:#1e2d4a'>", unsafe_allow_html=True)

    # Status indicators
    _, _, bc_err = load_blockchain()
    _, _, _, _, ml_err = load_ml_artifacts()

    bc_ok = bc_err is None
    ml_ok = ml_err is None

    st.markdown("**System Status**")
    st.markdown(
        f"{'🟢' if ml_ok else '🔴'} AI Model — {'Ready' if ml_ok else 'Not loaded'}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"{'🟢' if bc_ok else '🟡'} Blockchain — {'Connected' if bc_ok else 'Offline'}",
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#1e2d4a'>", unsafe_allow_html=True)
    st.markdown("**Settings**")
    auto_store = st.toggle("Auto-store safe emails", value=True,
                            help="Automatically push safe email hashes to blockchain after detection")
    show_probs  = st.toggle("Show confidence scores", value=True)

    if not bc_ok:
        st.markdown("<div class='warn-box'>⚠️ Blockchain offline.<br>Start Ganache on port 7545 to enable storage.</div>",
                    unsafe_allow_html=True)
    if not ml_ok:
        st.markdown(f"<div class='warn-box'>⚠️ {ml_err}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e2d4a'>", unsafe_allow_html=True)
    st.markdown("<small style='color:#475569'>AI + Blockchain Phishing Detection<br>Hybrid Model Project</small>",
                unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN LAYOUT — tabs
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("# 🛡️ CrypPhish AI")
st.markdown("<p style='color:#64748b;margin-top:-0.5rem'>AI-powered phishing detection with blockchain verification</p>",
            unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e2d4a'>", unsafe_allow_html=True)

tab_detect, tab_history, tab_verify = st.tabs([
    "🔍  Detect Email",
    "⛓️  Blockchain History",
    "✅  Verify Email",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DETECT
# ══════════════════════════════════════════════════════════════════════════════
with tab_detect:
    col_input, col_result = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.markdown("### 📨 Email Input")

        input_mode = st.radio("Input method", ["Paste text", "Upload .eml / .txt file"],
                               horizontal=True, label_visibility="collapsed")

        sender_val  = ""
        subject_val = ""
        body_val    = ""

        if input_mode == "Paste text":
            sender_val  = st.text_input("From (optional)", placeholder="sender@example.com")
            subject_val = st.text_input("Subject (optional)", placeholder="Email subject line")
            body_val    = st.text_area("Email body", height=260,
                                        placeholder="Paste the full email content here…")
        else:
            uploaded = st.file_uploader("Upload email file", type=["eml", "txt"])
            if uploaded:
                raw = uploaded.read()
                if uploaded.name.lower().endswith(".eml"):
                    parsed      = parse_eml_bytes(raw)
                    sender_val  = parsed["sender"]
                    subject_val = parsed["subject"]
                    body_val    = parsed["body"]
                    st.success(f"Parsed: **{uploaded.name}**")
                    st.caption(f"From: {sender_val}  |  Subject: {subject_val}")
                else:
                    body_val = raw.decode(errors="ignore")
                    st.success(f"Loaded: **{uploaded.name}**")

        detect_btn = st.button("🔍 Analyse Email", use_container_width=True,
                                disabled=not ml_ok or not body_val.strip())

    with col_result:
        st.markdown("### 📊 Analysis Result")

        if "last_result" not in st.session_state:
            st.markdown("""
            <div class='card' style='text-align:center;padding:3rem 1.5rem'>
                <div style='font-size:3rem;margin-bottom:1rem'>🔍</div>
                <div style='color:#475569'>Paste an email and click <b>Analyse</b> to see the result</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            r = st.session_state["last_result"]
            is_safe = r["label"] == "safe"
            card_cls  = "card-safe"  if is_safe else "card-phishing"
            badge_cls = "badge-safe" if is_safe else "badge-phishing"
            icon      = "✅"         if is_safe else "⚠️"
            title     = "SAFE"       if is_safe else "PHISHING"

            st.markdown(f"""
            <div class='card {card_cls}'>
                <div style='font-size:2.5rem;margin-bottom:0.5rem'>{icon}</div>
                <div class='{badge_cls}'>{title}</div>
                <div style='color:#94a3b8;font-size:0.85rem;margin-top:0.75rem'>
                    Confidence: <b style='color:#e2e8f0'>{r["confidence"]*100:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if show_probs and r.get("probs"):
                st.markdown("**Class Probabilities**")
                for lbl, prob in sorted(r["probs"].items(), key=lambda x: -x[1]):
                    col_lbl, col_bar = st.columns([1, 3])
                    with col_lbl:
                        st.markdown(f"<div style='font-size:0.8rem;color:#94a3b8;padding-top:6px'>{lbl}</div>",
                                    unsafe_allow_html=True)
                    with col_bar:
                        color = "#166534" if lbl == "safe" else "#7f1d1d"
                        st.markdown(
                            f"""<div style='background:#1e2d4a;border-radius:4px;height:18px;margin-top:4px'>
                                  <div style='background:{"#22c55e" if lbl=="safe" else "#ef4444"};
                                              width:{prob*100:.1f}%;height:100%;border-radius:4px;
                                              display:flex;align-items:center;padding-left:6px;
                                              font-size:0.72rem;color:white;font-weight:600'>
                                    {prob*100:.1f}%
                                  </div>
                                </div>""",
                            unsafe_allow_html=True,
                        )

            # Hash
            st.markdown(f"<div style='font-size:0.78rem;color:#64748b;margin:0.75rem 0 0.25rem'>SHA-256 Hash</div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='hash-box'>{r['hash']}</div>", unsafe_allow_html=True)

            # Blockchain result
            if r.get("tx_hash"):
                st.markdown("<div style='font-size:0.78rem;color:#64748b;margin:0.75rem 0 0.25rem'>⛓️ Blockchain Tx</div>",
                            unsafe_allow_html=True)
                st.markdown(f"<div class='tx-box'>{r['tx_hash']}</div>", unsafe_allow_html=True)
            elif r.get("bc_err"):
                st.markdown(f"<div class='warn-box'>Blockchain: {r['bc_err']}</div>",
                            unsafe_allow_html=True)
            elif r["label"] == "phishing":
                st.markdown("<div class='warn-box'>🚫 Phishing email — not stored on blockchain.</div>",
                            unsafe_allow_html=True)

    # ── Run detection ──────────────────────────────────────────────────────────
    if detect_btn and body_val.strip():
        with st.spinner("Analysing email…"):
            label, confidence, probs, err = predict(body_val)

        if err:
            st.error(f"Model error: {err}")
        else:
            email_hash = hashlib.sha256(body_val.encode("utf-8")).hexdigest()
            tx_hash    = None
            bc_err_msg = None

            if label == "safe" and auto_store and bc_ok:
                with st.spinner("Storing hash on blockchain…"):
                    tx_hash, bc_err_msg = store_on_blockchain(
                        email_hash,
                        sender_val  or "unknown",
                        subject_val or "No Subject",
                        label
                    )

            st.session_state["last_result"] = {
                "label":      label,
                "confidence": confidence,
                "probs":      probs,
                "hash":       email_hash,
                "tx_hash":    tx_hash,
                "bc_err":     bc_err_msg,
                "sender":     sender_val,
                "subject":    subject_val,
            }
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BLOCKCHAIN HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown("### ⛓️ Stored Email Records")

    if not bc_ok:
        st.markdown(f"<div class='warn-box'>{bc_err}</div>", unsafe_allow_html=True)
    else:
        if st.button("🔄 Refresh"):
            st.cache_resource.clear()

        records, err = fetch_blockchain_history()

        if err:
            st.error(f"Blockchain error: {err}")
        elif not records:
            st.markdown("<div class='info-box'>No emails stored yet. Analyse a safe email first.</div>",
                        unsafe_allow_html=True)
        else:
            # Summary metrics
            total   = len(records)
            safe_n  = sum(1 for r in records if r["prediction"].lower() == "safe")
            phish_n = total - safe_n

            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class='card' style='text-align:center'>
                    <div class='metric-value'>{total}</div>
                    <div class='metric-label'>Total Records</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class='card' style='text-align:center'>
                    <div class='metric-value' style='color:#22c55e'>{safe_n}</div>
                    <div class='metric-label'>Safe Emails</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class='card' style='text-align:center'>
                    <div class='metric-value' style='color:#ef4444'>{phish_n}</div>
                    <div class='metric-label'>Phishing (flagged)</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr style='border-color:#1e2d4a'>", unsafe_allow_html=True)

            for r in records:
                is_safe = r["prediction"].lower() == "safe"
                icon    = "✅" if is_safe else "⚠️"
                color   = "#22c55e" if is_safe else "#ef4444"
                with st.expander(f"{icon}  #{r['id']} — {r['subject'][:60]}  |  {r['timestamp']}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**From:** {r['sender']}")
                        st.markdown(f"**Prediction:** <span style='color:{color}'>{r['prediction'].upper()}</span>",
                                    unsafe_allow_html=True)
                        st.markdown(f"**Stored at:** {r['timestamp']}")
                    with c2:
                        st.markdown("**Email Hash (SHA-256)**")
                        st.markdown(f"<div class='hash-box'>{r['hash']}</div>",
                                    unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — VERIFY
# ══════════════════════════════════════════════════════════════════════════════
with tab_verify:
    st.markdown("### ✅ Verify an Email on Blockchain")
    st.markdown("""
    <div class='info-box'>
    Paste an email body below. The system will compute its SHA-256 hash and
    check whether that hash is recorded on the blockchain, confirming the email
    was previously classified as <b>safe</b>.
    </div>
    """, unsafe_allow_html=True)

    verify_text = st.text_area("Email body to verify", height=200,
                                placeholder="Paste the exact email body here…")

    if st.button("🔎 Verify on Blockchain", disabled=not bc_ok or not verify_text.strip()):
        query_hash = hashlib.sha256(verify_text.encode("utf-8")).hexdigest()
        st.markdown(f"<div class='hash-box' style='margin-bottom:1rem'>🔑 {query_hash}</div>",
                    unsafe_allow_html=True)

        records, err = fetch_blockchain_history()
        if err:
            st.error(err)
        else:
            match = next((r for r in records if r["hash"] == query_hash), None)
            if match:
                st.markdown(f"""
                <div class='card card-safe' style='padding:1.5rem'>
                    <div style='font-size:1.5rem;margin-bottom:0.5rem'>✅ Found on Blockchain</div>
                    <table style='width:100%;color:#e2e8f0;font-size:0.9rem'>
                        <tr><td style='color:#64748b;width:120px'>Record #</td><td>{match['id']}</td></tr>
                        <tr><td style='color:#64748b'>From</td><td>{match['sender']}</td></tr>
                        <tr><td style='color:#64748b'>Subject</td><td>{match['subject']}</td></tr>
                        <tr><td style='color:#64748b'>Classification</td>
                            <td style='color:#22c55e;font-weight:700'>{match['prediction'].upper()}</td></tr>
                        <tr><td style='color:#64748b'>Stored at</td><td>{match['timestamp']}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='card card-phishing' style='padding:1.5rem'>
                    <div style='font-size:1.5rem;margin-bottom:0.5rem'>❌ Not Found</div>
                    <div style='color:#94a3b8'>This email hash is not recorded on the blockchain.
                    It was either classified as phishing, or has not been analysed yet.</div>
                </div>
                """, unsafe_allow_html=True)
