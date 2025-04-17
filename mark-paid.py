import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
client = gspread.authorize(credentials)

spreadsheet = client.open("Boletos Loja")
sheet = spreadsheet.worksheet("Página1")

doc_number = input("Número do documento que deseja marcar como pago: ").strip()

records = sheet.get_all_records()

matches = []
for idx, row in enumerate(records, start=2):  # start=2 to skip header
    if str(row["Número do Documento"]) == doc_number:
        matches.append({
            "row": idx,
            "installment": row["Parcelas"],
            "status": row["Situação"]
        })

if not matches:
    print(f"❌ Documento {doc_number} não encontrado.")
    exit()

print(f"Encontrado {len(matches)} parcelas:")
for m in matches:
    print(f"- Linha {m['row']} | Parcela: {m['installment']} | Status: {m['status']}")

selected_number = input("Qual parcela deseja marcar como pago? (Digite apenas o número. Ex: 2 para parcela 02/XX): ").strip()

updated = False
for m in matches:
    installment_number = m["installment"].split("/")[0].lstrip("0")
    if installment_number == selected_number:
        sheet.update_acell(f"H{m['row']}", datetime.today().strftime("%d/%m/%Y"))
        sheet.update_acell(f"J{m['row']}", "Pago")
        updated = True
        print(f"✅ Parcela {m['installment']} marcada como paga.")
        break

if not updated:
    print(f"❌ Parcela {selected_number} não encontrada para o documento {doc_number}.")
