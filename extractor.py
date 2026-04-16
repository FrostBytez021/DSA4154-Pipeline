import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

# Load credentials from the environment variable (GitHub Secret)
creds_json = os.environ.get("GCP_CREDENTIALS")
if creds_json is None:
    raise ValueError("Missing GCP_CREDENTIALS environment variable")

creds_dict = json.loads(creds_json)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# (The rest of your code stays exactly the same!)
sheet = client.open("DSA4154_Dummy_DB").sheet1
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
dummy_row = [current_time, "Pipeline Test", "Status: GitHub Action Success!"]
sheet.append_row(dummy_row)

print("Success! Data pushed from GitHub Actions.")