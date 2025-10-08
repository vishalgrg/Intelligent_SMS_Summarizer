import re

def clean_sms(text):
    text = re.sub(r'[A-Z]{2}-[A-Z0-9]+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower().strip()
