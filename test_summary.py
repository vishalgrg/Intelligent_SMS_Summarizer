from utils.categorize import categorize_sms_list
from collections import Counter

# Step 1: List of test SMS messages
test_sms = [
    "Recharge now and get 2GB free data",
    "Your SBI credit card bill is due soon",
    "50% off on domestic flights this weekend",
    "Flat 30% discount on Amazon fashion sale",
    "Watch the latest movie releases on Hotstar",
    "Recharge Rs.399 and get extra validity",
    "Banking alert: Rs.500 credited to your account",
    "Book hotel with 10% cashback",
    "New music album released on Spotify",
]

# Step 2: Categorize each SMS
categories = categorize_sms_list(test_sms)

# Step 3: Count categories
counts = Counter(categories)

# Step 4: Generate readable summary
summary = ", ".join([f"{count} {cat}" for cat, count in counts.items()])

# Step 5: Print results
print("Individual SMS Categories:")
for sms, cat in zip(test_sms, categories):
    print(f"- {sms} --> {cat}")

print("\nDaily Summary:")
print(summary)
