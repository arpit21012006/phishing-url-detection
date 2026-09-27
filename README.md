# 🔐 Phishing URL Detection System

A Machine Learning-based web application that analyzes URLs and predicts whether they are **Safe, Suspicious, or Dangerous**.

The application combines a trained Machine Learning model with a Flask backend and an interactive
 web interface to provide real-time URL risk assessment.

## 🚀 Features

- 🔍 Real-time URL scanning
- 🤖 Machine Learning-based phishing detection
- 📊 URL risk score
- 🟢 Safe, 🟡 Suspicious, and 🔴 Dangerous classification
- 🌐 Simple and responsive web interface
- ⚡ Flask-based backend API
- 📁 Trained model and vectorizer integration
- 🛡️ Handles malformed URLs safely

## 🧠 How It Works

1. The user enters a URL in the web interface.
2. The URL is sent to the Flask `/predict` endpoint.
3. The trained ML model analyzes the URL.
4. The application calculates a risk score.
5. The result is displayed as **Safe, Suspicious, or Dangerous**.

## 🛠️ Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- Flask

**Machine Learning**
- Scikit-learn
- Pandas
- Multinomial Naive Bayes
- URL vectorization

**Development Tools**
- VS Code
- Jupyter Notebook
- Git
- GitHub

## 📂 Project Structure

```text
phishing-url-detection/
│
├── app.py
├── requirements.txt
├── phishing_mnb.pkl
├── vectorizer.pkl
├── dataset/
│   └── phishing_site_urls.csv
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── blog.html
│   └── contact.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/arpit21012006/phishing-url-detection.git
```

Move into the project directory:

```bash
cd phishing-url-detection
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 🧪 Example

Enter a URL such as:

```text
https://www.google.com
```

The system analyzes the URL and displays its predicted risk level and risk score.

> **Note:** This project is intended for educational and research purposes. Machine-learning predictions 
should not be treated as a replacement for professional security analysis.

## 🔮 Future Improvements

- Improve model accuracy using advanced ML algorithms
- Add additional URL and domain-based security features
- Integrate external threat-intelligence APIs
- Add URL scan history
- Improve phishing explanation and detection insights
- Deploy the application for public access

## 👨‍💻 Author

**Arpit Sharma**

B.Tech(hons. Cyber security) Computer Science & Engineering(Data Science) Student  
Interested in, Data Science and Cybersecurity

GitHub: `@arpit21012006`

---

⭐ If you find this project useful, consider giving the repository a star.
