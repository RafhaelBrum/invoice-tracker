import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def send_to_google_sheets(df: pd.DataFrame):
    credentials_path = "config/credentials.json"

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("Boletos Loja")
    worksheet = spreadsheet.worksheet("Página1")

    values = df.values.tolist()

    worksheet.append_rows(values, value_input_option="USER_ENTERED")

    print("✅ Dados enviados com sucesso.")

def get_existing_document_numbers():
    credentials_path = "config/credentials.json"
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("Boletos Loja")
    worksheet = spreadsheet.worksheet("Página1")

    all_data = worksheet.get_all_records()

    return [str(row["Número do Documento"]).strip() for row in all_data if "Número do Documento" in row]