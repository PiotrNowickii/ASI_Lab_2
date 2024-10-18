import pandas as pd
import logging
import gspread
from google.oauth2.service_account import Credentials


if __name__ == "__main__":
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
    sheet_id = "1-TdYTmaMyK7mPncbZE4wEiFPirj8itMS9H9s9YdKwaQ"
    worksheet = client.open_by_key(sheet_id).sheet1
    df = pd.read_csv("Lab2---Obr-bka-danych/data_student_24667.csv")
    #df = df.where(pd.notnull(df), None)
    #data = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    #worksheet.append_rows(data)
    
    