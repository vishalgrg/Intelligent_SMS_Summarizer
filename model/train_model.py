import pandas as pd
import os
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# 1. Set dataset path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sms_dataset.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

# Load dataset
df = pd.read_csv(DATA_PATH)
print(f"Loaded dataset with {len(df)} messages.")
print("Columns in CSV:", df.columns.tolist())

# -----------------------------
# 2. Handle missing data
# -----------------------------
# Ensure correct column names
if 'message' not in df.columns:
    if 'Message' in df.columns:
        df.rename(columns={'Message': 'message'}, inplace=True)
    else:
        raise KeyError("CSV must have a 'message' column")

if 'category' not in df.columns:
    if 'Category' in df.columns:
        df.rename(columns={'Category': 'category'}, inplace=True)
    else:
        raise KeyError("CSV must have a 'category' column")

# Drop rows with missing messages or categories
df = df.dropna(subset=['message', 'category']).reset_index(drop=True)
print(f"Dataset after dropping missing values: {len(df)} messages.")

# -----------------------------
# 3. Text preprocessing
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)                 # Remove URLs
    text = re.sub(r"[^a-z0-9₹% ]", " ", text)          # Keep letters, digits, ₹, %, space
    text = re.sub(r"\s+", " ", text).strip()           # Remove extra spaces
    return text

df['cleaned'] = df['message'].apply(clean_text)

# Drop any messages that became empty after cleaning
df = df[df['cleaned'] != ""].reset_index(drop=True)
print(f"Dataset after cleaning: {len(df)} messages.")

# -----------------------------
# 4. Split dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned'], df['category'],
    test_size=0.2,
    random_state=42,
    stratify=df['category']
)

# -----------------------------
# 5. Feature extraction
# -----------------------------
vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    max_features=10000,
    stop_words='english'
)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# -----------------------------
# 6. Train model
# -----------------------------
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# -----------------------------
# 7. Evaluate
# -----------------------------
y_pred = model.predict(X_test_vect)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model accuracy: {accuracy:.2f}\n")
print("Classification report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# 8. Save model & vectorizer
# -----------------------------
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, "classifier.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print(f"Model and vectorizer saved successfully in {MODEL_DIR}.")
