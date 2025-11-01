**Intelligent SMS Summarizer**

About the Idea

Intelligent SMS Summarizer is an AI-powered system that helps users automatically manage and understand promotional SMS messages.
It reads raw SMS text, classifies them into categories such as Recharge Offers, Banking & Finance, Travel Deals, E-commerce, and Entertainment, and then generates a clean daily digest like:

**“3 Recharge Offers, 2 Travel Deals, 1 Banking Update”**

The goal is to reduce message clutter and provide users with meaningful, summarized insights instead of hundreds of unread SMS.

🚀 Features Implemented

**1. Machine Learning-based SMS Categorization**

Uses TF-IDF Vectorization + Naive Bayes model for accurate text classification.

Trained on a realistic dataset of 5000+ SMS messages.

Achieves ~100% accuracy on labeled training data (train_model.py).

Supports the following 5 categories:

* Recharge Offers

* Banking & Finance

* Travel Deals

* E-commerce / Shopping

* Entertainment


**2. Automatic Text Cleaning & Preprocessing**

Removes unwanted characters, punctuation, and symbols.

Converts messages to lowercase for normalized processing.

Handles empty or malformed data entries gracefully.

**3. Daily Digest Generation**

Groups classified SMS by category.

Generates a concise daily summary showing message count per category.

**Example:**

3 Recharge Offers, 1 Travel Deal, 2 Banking Updates

**4. Interactive Dashboard (Flask + HTML + Nokia Theme)**

Responsive UI with Nokia color palette.

**Users can:**

* Paste SMS messages manually.

* Click Generate Digest to analyze and classify.

* Filter and search by category or keyword.

Implemented in dashboard.html.

**5. Flask Backend API**

Modular backend (app.py) built with Flask 3.0.

Handles SMS input, categorization, and digest creation.

Ready for API extensions like:

/categorize → classify messages

/summary → generate digest

/metrics → monitor performance

**6. Dual-Source Nokia Logo**

Automatically loads logo from the Nokia internal URL.

Falls back to local file (static/images/nokia_logo.png) when offline.

Ensures consistent branding both inside and outside the Nokia network.

**Future Enhancements**

AI-based Summarization using Transformer models (T5 / BART) for short, user-friendly text summaries.

Real-time SMS ingestion via Android app or cloud API.

Metrics Dashboard using Prometheus & Grafana.

OAuth2-based login for user personalization.

Docker & Kubernetes deployment for production scalability.

🧩 System Architecture (HLD)

1️⃣ Input Layer

SMS messages entered by users or fetched from device.

CSV dataset used for model training.

2️⃣ Processing Layer

Text Cleaning & Normalization

TF-IDF Vectorization

Naive Bayes Classification

Flask API endpoints for integration

3️⃣ Presentation Layer

Nokia-themed HTML Dashboard

Daily digest view with filters & search

4️⃣ Storage & Deployment

classifier.pkl and vectorizer.pkl saved locally

Dataset stored in model/data/sms_dataset.csv

Flask runs locally; ready for GCP or Docker deployment

5️⃣ Monitoring (Next Phase)

Prometheus + Grafana for performance metrics and insights

**⚙️ Setup Instructions**

**1. Clone the repository**
git clone https://github.com/vishalgrg/Intelligent_SMS_Summarizer.git

cd intelligent-sms-summarizer

**2️. Create and activate a virtual environment**

python -m venv .venv
# Activate
.venv\Scripts\activate        # Windows

source .venv/bin/activate     # Linux/macOS

**3.Install dependencies**

pip install -r requirements.txt

🧠 Train the Model (in case you want to train with your own data)

python model/train_model.py

**This script:**

* Loads data from model/data/sms_dataset.csv
* Preprocesses text
* Trains the Naive Bayes model
* Saves classifier.pkl and vectorizer.pkl

**💻 Run the Web App**

python app.py

Then open your browser and go to:
 http://127.0.0.1:5000

**Sample data you can take from this file:-** 
https://github.com/vishalgrg/Intelligent_SMS_Summarizer/blob/master/data/sms_dataset.csv 

**Dashboard Features**

* Paste SMS → click Generate Digest
* View categorized messages by section
* Search or filter by category
* Nokia logo loads dynamically (internal + local)
