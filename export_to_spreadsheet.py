import pandas as pd
import logging
import gspread
from google.oauth2.service_account import Credentials


def main():
    scope = ["https://googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
    sheet_id = "1-TdYTmaMyK7mPncbZE4wEiFPirj8itMS9H9s9YdKwaQ"
    worksheet = client.open_by_key(sheet_id).sheet1
    df = pd.read_csv("Lab2---Obr-bka-danych/data_student_24667")
    data = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.append_rows(data)
    
    