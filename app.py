from flask import Flask, request, jsonify
from collections import Counter
#from utils.categorize import categorize_sms_list
from utils.categorize import categorize_sms_list

app = Flask(__name__)

@app.route('/')
def index():
    return "Intelligent SMS Summarizer API is running!"

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    sms_list = data.get('messages', [])
    if not sms_list:
        return jsonify({"error": "No messages provided"}), 400

    predictions = categorize_sms_list(sms_list)
    summary = Counter(predictions)

    summary_text = ", ".join([f"{count} {category}" for category, count in summary.items()])
    return jsonify({
        "summary": summary_text,
        "category_counts": summary
    })

if __name__ == '__main__':
    app.run(debug=True)
