import pickle
from utils.preprocess import clean_sms

# Load model and vectorizer
model = pickle.load(open('model/classifier.pkl', 'rb'))
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))

def categorize_sms_list(sms_list):
    cleaned = [clean_sms(s) for s in sms_list]
    X = vectorizer.transform(cleaned)
    preds = model.predict(X)
    return preds.tolist()