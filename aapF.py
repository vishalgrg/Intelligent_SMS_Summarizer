from flask import Flask, render_template, request, Response
from utils.categorize import categorize_sms_list
from collections import defaultdict
import pandas as pd
import os, datetime
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# -----------------------------
# Dataset
# -----------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sms_dataset.csv")
df = pd.read_csv(DATA_PATH)
all_sms = df['message'].tolist()

# -----------------------------
# Category colors
# -----------------------------
CATEGORY_COLORS = {
    "Recharge Offers": "#FFB347",
    "Banking & Finance": "#77DD77",
    "Travel Deals": "#89CFF0",
    "E-commerce": "#FFD700",
    "Entertainment": "#FF6961",
}

# -----------------------------
# Prometheus metrics
# -----------------------------
sms_total = Counter("sms_total_processed", "Total SMS processed")
category_sms_count = Gauge("category_sms_count", "Number of SMS per category", ["category"])

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# -----------------------------
# Digest & metrics
# -----------------------------
def generate_daily_digest(sms_list, filter_category=None, search_keyword=None):
    if search_keyword:
        sms_list = [sms for sms in sms_list if search_keyword.lower() in sms.lower()]

    categories = categorize_sms_list(sms_list)

    category_dict = defaultdict(list)
    for sms, cat in zip(sms_list, categories):
        category_dict[cat].append(sms)

    if filter_category:
        category_dict = {cat: msgs for cat, msgs in category_dict.items() if cat == filter_category}

    today = datetime.date.today().strftime("%d-%b-%Y")
    digest = {"date": today, "categories": []}
    for cat, msgs in category_dict.items():
        digest["categories"].append({"category": cat, "count": len(msgs), "messages": msgs})

    # Update Prometheus metrics
    sms_total.inc(len(sms_list))
    for cat_info in digest['categories']:
        safe_label = cat_info['category'].replace(" ", "_")
        category_sms_count.labels(category=safe_label).set(cat_info['count'])

    return digest

# -----------------------------
# Dashboard route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def dashboard():
    sms_list = all_sms
    filter_category = None
    search_keyword = None

    if request.method == "POST":
        search_keyword = request.form.get("search_keyword")
        filter_category = request.form.get("filter_category")
        sms_text = request.form.get("sms_text")
        if sms_text:
            sms_list = [line.strip() for line in sms_text.split("\n") if line.strip()]

    digest = generate_daily_digest(sms_list, filter_category, search_keyword)
    categories = sorted(list(set(df['category'])))

    return render_template("dashboard.html", digest=digest, sms_list=sms_list,
                           categories=categories, selected_category=filter_category,
                           search_keyword=search_keyword, category_colors=CATEGORY_COLORS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
