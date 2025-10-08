import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# -----------------------------
# 1. Set dataset path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current folder
DATA_PATH = os.path.join(BASE_DIR, "data", "sms_dataset.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

# -----------------------------
# 2. Preprocess SMS text
# -----------------------------
df['cleaned'] = df['message'].str.lower()

# -----------------------------
# 3. Split dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned'], df['category'], test_size=0.2, random_state=42
)

# -----------------------------
# 4. Feature extraction
# -----------------------------
vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# -----------------------------
# 5. Train model
# -----------------------------
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# -----------------------------
# 6. Evaluate model
# -----------------------------
y_pred = model.predict(X_test_vect)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# -----------------------------
# 7. Save model & vectorizer
# -----------------------------
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)  # <-- ensures folder exists

with open(os.path.join(MODEL_DIR, "classifier.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")
