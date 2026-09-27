from flask import Flask, render_template, request, jsonify
import pickle
import re
import csv
from urllib.parse import urlparse, unquote
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

VECTOR_PATH = BASE_DIR / "vectorizer.pkl"
MODEL_PATH = BASE_DIR / "phishing.pkl"
PHISHING_CSV_PATH = BASE_DIR / "dataset" / "phishing_site_urls.csv"


# =========================================================
# LOAD ML FILES
# =========================================================

def _load_pickle(path: Path):
    if not path.exists():
        raise RuntimeError(
            f"Required file not found: {path}. "
            f"Place the file next to app.py."
        )

    with open(path, "rb") as f:
        return pickle.load(f)


vector = _load_pickle(VECTOR_PATH)
model = _load_pickle(MODEL_PATH)


# =========================================================
# URL NORMALIZATION FOR DATASET MATCHING
# =========================================================

def _normalize_for_matching(raw: str) -> str:

    if raw is None:
        return ""

    s = str(raw).strip()

    if not s:
        return ""

    # Remove surrounding quotes
    if (
        (s.startswith("'") and s.endswith("'"))
        or
        (s.startswith('"') and s.endswith('"'))
    ):
        s = s[1:-1].strip()

    s = unquote(s)

    # Add protocol if missing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", s):
        s = "http://" + s

    try:
        p = urlparse(s)
        host = (p.hostname or "").strip().lower()
    except ValueError:
         return ""
    path = (p.path or "").strip()
    query = (p.query or "").strip()

    if path.endswith("/") and path != "/":
        path = path[:-1]

    matched = host + path

    if query:
        matched += "?" + query

    return matched


# =========================================================
# LOAD PHISHING URL DATASET
# =========================================================

def _load_phishing_list():

    phishing_set = set()

    try:

        with open(
            PHISHING_CSV_PATH,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                url = row.get("URL") or row.get("url")

                label = (
                    row.get("Label")
                    or row.get("label")
                    or ""
                ).strip().lower()

                if not url:
                    continue

                if label == "bad":
                    phishing_set.add(
                        _normalize_for_matching(url)
                    )

    except FileNotFoundError:
        print("Warning: phishing dataset not found.")

    except Exception as e:
        print("Dataset loading error:", e)

    phishing_set.discard("")

    return phishing_set


PHISHING_URLS_SET = _load_phishing_list()


# =========================================================
# ML URL PREPROCESSING
# =========================================================
def normalize_url_for_ml(raw: str) -> str:
    if raw is None:
        return ""

    url = raw.strip().lower()

    if not url:
        return ""

    # Remove protocol because model was trained mainly on URL tokens
    url = re.sub(r"^https?://", "", url)

    # Extract alphabetic tokens
    tokens = re.findall(r"[A-Za-z]+", url)

    try:
        from nltk.stem.snowball import SnowballStemmer
        stemmer = SnowballStemmer("english")
        tokens = [stemmer.stem(t) for t in tokens]
    except Exception:
        tokens = [t.lower() for t in tokens]

    return " ".join(tokens)


# =========================================================
# ML PREDICTION
# =========================================================

def predict_url_ml(cleaned_url: str):

    if not cleaned_url:
        return None, "Please enter a valid URL.", 0

    transformed_url = vector.transform([cleaned_url])

    pred = model.predict(transformed_url)[0]

    if pred == "bad":

        return (
            pred,
            "This is a Phishing website !!",
            85
        )

    elif pred == "good":

        return (
            pred,
            "This is a healthy and safe website.",
            15
        )

    return (
        pred,
        "Unable to determine website safety.",
        50
    )


# =========================================================
# FINAL URL PREDICTION
# =========================================================

def predict_url(url_raw: str):
    normalized_match = _normalize_for_matching(url_raw)

    print("\n========== SCAN DEBUG ==========")
    print("RAW URL:", url_raw)
    print("LIST NORMALIZED:", normalized_match)
    print("IN PHISHING LIST:", normalized_match in PHISHING_URLS_SET)

    if normalized_match and normalized_match in PHISHING_URLS_SET:
        print("RESULT SOURCE: CSV phishing list")
        print("===============================\n")
        return "bad", "This is a Phishing website !!", 95

    cleaned_url = normalize_url_for_ml(url_raw)

    print("ML INPUT:", cleaned_url)

    X = vector.transform([cleaned_url])
    prediction = model.predict(X)[0]

    print("MODEL PREDICTION:", prediction)

    if hasattr(model, "predict_proba"):
        print("PROBABILITY:", model.predict_proba(X))

    print("RESULT SOURCE: ML model")
    print("===============================\n")

    return predict_url_ml(cleaned_url)

# =========================================================
# WEBSITE ROUTES
# =========================================================

# HOME PAGE
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        url = request.form.get(
            "url",
            ""
        )

        label, verdict, risk_score = predict_url(
            url
        )

        return render_template(
            "index.html",
            predict=verdict,
            risk_score=risk_score,
            label=label
        )

    return render_template(
        "index.html",
        risk_score=0
    )


# ABOUT PAGE
@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# BLOG PAGE
@app.route("/blog")
def blog():

    return render_template(
        "blog.html"
    )


# CONTACT PAGE
@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# API ENDPOINT
# =========================================================

@app.route("/predict", methods=["POST"])
def predict_endpoint():

    data = request.get_json(
        silent=True
    ) or {}

    url = data.get(
        "url",
        ""
    )

    label, verdict, risk_score = predict_url(
        url
    )

    return jsonify({
        "label": label,
        "verdict": verdict,
        "risk_score": risk_score
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )