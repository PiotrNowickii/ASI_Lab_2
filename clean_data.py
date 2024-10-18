import pandas as pd
import logging
import gspread
import random
from sklearn.preprocessing import StandardScaler
from google.oauth2.service_account import Credentials

def random_travel_time():
        start_hour = random.randint(5, 23)
        start_minute = random.randint(0, 59)
        duration = random.uniform(0.1, 12)
        end_hour = (start_hour + int(duration)) % 24
        end_minute = (start_minute + int((duration % 1) * 60)) % 60
        return f"{start_hour:02}:{start_minute:02}", f"{end_hour:02}:{end_minute:02}"

if __name__ == "__main__":
    logging.basicConfig(filename='log.txt',filemode='w',level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Began retrieving data from google spreadsheet')
    genders = ['Mężczyzna', 'Kobieta']
    education_levels = ['Podstawowe', 'Średnie', 'Wyższe']
    travel_goals = ['Praca', 'Zakupy', 'Edukacja', 'Rozrywka', 'Inne']
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
    sheet_id = "1-TdYTmaMyK7mPncbZE4wEiFPirj8itMS9H9s9YdKwaQ"
    worksheet = client.open_by_key(sheet_id).sheet1
    df = pd.read_csv("Lab2---Obr-bka-danych/data_student_24667.csv")
    logger.info('Finished retrieving data from csv')
    length_before_collumn_drop = len(df)
    df = df.dropna(thresh=4)
    length_after_collumn_drop = len(df)
    removed_rows = length_before_collumn_drop - length_after_collumn_drop
    filled_rows = 0
    
    logger.info('Began cleaning data')
    filled_rows += df['Płeć'].isna().sum()
    df.loc[df['Płeć'].isna(), 'Płeć'] = random.choice(genders)
    filled_rows += df['Wiek'].isna().sum()
    df.loc[df['Wiek'].isna(), 'Wiek'] = df['Wiek'].median()
    filled_rows += df['Wykształcenie'].isna().sum()
    df.loc[df['Wykształcenie'].isna(), 'Wykształcenie'] = random.choice(education_levels)
    filled_rows += df['Średnie Zarobki'].isna().sum()
    df.loc[df['Średnie Zarobki'].isna(), 'Średnie Zarobki'] = df['Średnie Zarobki'].median()
    filled_rows += df['Czas Początkowy Podróży'].isna().sum()
    start_time, end_time = random_travel_time()
    df.loc[df['Czas Początkowy Podróży'].isna(), 'Czas Początkowy Podróży'] = start_time
    filled_rows += df['Czas Końcowy Podróży'].isna().sum()
    df.loc[df['Czas Końcowy Podróży'].isna(), 'Czas Końcowy Podróży'] = end_time
    filled_rows += df['Cel Podróży'].isna().sum()
    df.loc[df['Cel Podróży'].isna(), 'Cel Podróży'] = random.choice(travel_goals)
    logger.info('Finished cleaning data')

    logger.info('Began the standardization of data')
    scaler = StandardScaler()
    df.loc[:, ['Wiek', 'Średnie Zarobki']] = scaler.fit_transform(df.loc[:, ['Wiek', 'Średnie Zarobki']])
    logger.info('Finished the standardization of data')

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    logger.info('Saved data to sheet')

    removed_percent = (removed_rows/length_before_collumn_drop) * 100
    filled_percent = (filled_rows/length_after_collumn_drop) * 100
    

    with open("report.txt", "w") as file:
        file.write(f"Percent of removed rows: {removed_percent:.2f}%\nPercent of changed rows: {filled_percent:.2f}%")
    logger.info(f"Removed {removed_rows} rows")
    logger.info(f"Filled empty data of {filled_rows} rows")
    