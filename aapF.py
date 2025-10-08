from flask import Flask, render_template, request
from utils.categorize import categorize_sms_list
from collections import defaultdict
import pandas as pd
import os
import datetime

app = Flask(__name__)

# -----------------------------
# Load dataset
# -----------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sms_dataset.csv")
df = pd.read_csv(DATA_PATH)
all_sms = df['message'].tolist()

# -----------------------------
# Category color mapping
# -----------------------------
CATEGORY_COLORS = {
    "Recharge Offers": "#FFB347",
    "Banking & Finance": "#77DD77",
    "Travel Deals": "#89CFF0",
    "E-commerce": "#FFD700",
    "Entertainment": "#FF6961",
}

# -----------------------------
# Generate digest function
# -----------------------------
def generate_daily_digest(sms_list, filter_category=None, search_keyword=None):
    # Apply search filter
    if search_keyword:
        sms_list = [sms for sms in sms_list if search_keyword.lower() in sms.lower()]

    # Categorize
    categories = categorize_sms_list(sms_list)

    # Group by category
    category_dict = defaultdict(list)
    for sms, cat in zip(sms_list, categories):
        category_dict[cat].append(sms)

    # Apply category filter
    if filter_category:
        category_dict = {cat: msgs for cat, msgs in category_dict.items() if cat == filter_category}

    # Prepare digest
    today = datetime.date.today().strftime("%d-%b-%Y")
    digest = {
        "date": today,
        "categories": []
    }

    for cat, msgs in category_dict.items():
        digest["categories"].append({
            "category": cat,
            "count": len(msgs),
            "messages": msgs
        })

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
    app.run(debug=True)
