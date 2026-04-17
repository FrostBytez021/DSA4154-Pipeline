import gspread
from google.oauth2.service_account import Credentials
import json
import os
import requests
import pandas as pd

# --- 1. DATA EXTRACTION (Your groupmate's API code) ---
url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=14.5995&longitude=120.9842&hourly=pm10,pm2_5&timezone=Asia%2FManila"
response = requests.get(url)
json_data = response.json()

hourly_data = json_data['hourly']
data = pd.DataFrame({
    "Time": hourly_data['time'],
    "PM10": hourly_data['pm10'],
    "PM2.5": hourly_data['pm2_5']
})

# Drop nulls (future hours) and get the latest 5 hours of data
clean_data = data.dropna().tail(5)

# Convert the pandas DataFrame into a list of lists so Google Sheets can read it
rows_to_append = clean_data.values.tolist()


# --- 2. GOOGLE SHEETS UPLOAD (Your pipeline code) ---
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# This checks if it's running on GitHub or running locally on your computer
creds_json = os.environ.get("GCP_CREDENTIALS")
if creds_json:
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
else:
    # If running on your computer for the demo, it finds your local file!
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)

client = gspread.authorize(creds)

# Make sure this matches your actual Google Sheet name!
sheet = client.open("DSA4154_Dummy_DB").sheet1 

# Append the real data!
sheet.append_rows(rows_to_append)

print(f"Success! Appended {len(rows_to_append)} rows of real PM10 and PM2.5 data to Google Sheets.")