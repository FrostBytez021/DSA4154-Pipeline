import gspread
from google.oauth2.service_account import Credentials
import json
import os
import requests
import pandas as pd

# --- 1. DATA EXTRACTION ---
stations = {
    "Caloocan(Univ. of East)": {"lat": 14.6581, "lon": 120.9842},
    "Las Pinas City": {"lat": 14.4445, "lon": 120.9939},
    "Makati": {"lat": 14.5632, "lon": 121.0565},
    "Malabon City": {"lat": 14.6681, "lon": 120.9658},
    "Mandaluyong": {"lat": 14.5794, "lon": 121.0359},
    "Manila City Hall": {"lat": 14.5895, "lon": 120.9816},
    "Marikina CEMO": {"lat": 14.6507, "lon": 121.1029},
    "Muntinlupa(Filinvest City)": {"lat": 14.4205, "lon": 121.0407},
    "Navotas": {"lat": 14.6732, "lon": 120.9416},
    "Paranaque City": {"lat": 14.4793, "lon": 121.0198},
    "Pasay": {"lat": 14.5378, "lon": 121.0014},
    "Pasig City": {"lat": 14.5764, "lon": 121.0851},
    "Quezon City(Ateneo)": {"lat": 14.6394, "lon": 121.0781},
    "Quezon City(SMPH Commonwealth)": {"lat": 14.6682, "lon": 121.0662},
    "San Juan City": {"lat": 14.6042, "lon": 121.0300},
    "Taguig (TUP)": {"lat": 14.5093, "lon": 121.0451},
    "Valenzuela": {"lat": 14.7000, "lon": 120.9833}
}

def get_remarks(aqi):
    if aqi <= 50: return "GOOD"
    elif aqi <= 100: return "FAIR"
    elif aqi <= 150: return "UNHEALTHY for sensitive groups"
    elif aqi <= 200: return "VERY UNHEALTHY"
    elif aqi <= 300: return "ACUTELY UNHEALTHY"
    else: return "EMERGENCY"

combined_records = []

for station, coords in stations.items():
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={coords['lat']}&longitude={coords['lon']}&current=pm10,pm2_5,us_aqi_pm2_5,us_aqi_pm10&timezone=Asia%2FManila"
    
    response = requests.get(url)
    json_data = response.json()
    
    current_data = json_data['current']
    time_recorded = current_data['time'] 
    
    pm10 = current_data['pm10']
    aqi_pm10 = current_data['us_aqi_pm10']
    remarks_pm10 = get_remarks(aqi_pm10)
    
    pm25 = current_data['pm2_5']
    aqi_pm25 = current_data['us_aqi_pm2_5']
    remarks_pm25 = get_remarks(aqi_pm25)
    
    combined_records.append([
        time_recorded, 
        station, 
        pm10, aqi_pm10, remarks_pm10, 
        pm25, aqi_pm25, remarks_pm25
    ])


# --- 2. TERMINAL VISUALIZATION FOR THE DEMO ---
# Creating a DataFrame just to print it beautifully to the terminal
headers = ["Time", "Station", "PM10", "AQI(PM10)", "Remarks(PM10)", "PM2.5", "AQI(PM2.5)", "Remarks(PM2.5)"]
demo_df = pd.DataFrame(combined_records, columns=headers)

print("\n" + "="*110)
print(" 📡 LIVE METRO MANILA AIR QUALITY DATA EXTRACTED ")
print("="*110)
print(demo_df.to_string(index=False))
print("="*110 + "\n")


# --- 3. GOOGLE SHEETS UPLOAD ---
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_json = os.environ.get("GCP_CREDENTIALS")
if creds_json:
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
else:
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)

client = gspread.authorize(creds)
sheet = client.open("DSA4154_Dummy_DB").sheet1 

sheet.append_rows(combined_records)
print(f"✅ Success! Appended {len(combined_records)} rows of live station data to Google Sheets.")