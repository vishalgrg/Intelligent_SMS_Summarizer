import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Load model and vectorizer
with open(os.path.join(MODEL_DIR, "classifier.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

def categorize_sms_list(sms_list):
    cleaned_sms = [sms.lower() for sms in sms_list]
    X_vect = vectorizer.transform(cleaned_sms)
    return model.predict(X_vect)
