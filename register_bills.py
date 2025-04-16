import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from send_to_sheets import send_to_google_sheets, get_existing_document_numbers


def register_bills():
    document_number = input("Número do Documento: ").strip()

    existing_documents = get_existing_document_numbers()
    if document_number in existing_documents:
        print(f"❌ Já existe uma entrada com o Número do Documento {document_number} no Google Sheets. Operação cancelada.")
        return

    supplier = input("Fornecedor: ")
    description = input("Descrição: ")
    installment_value = float(input("Valor da parcela (use ponto, ex: 300.00): "))
    total_installments = int(input("Número de parcelas: "))
    first_due_date_str = input("Data do 1º vencimento (formato DD/MM/AAAA): ")
    payment_method = input("Forma de pagamento (ex: Boleto, Pix): ")
    notes = input("Observações (pressione Enter se não tiver): ")

    first_due_date = datetime.strptime(first_due_date_str, "%d/%m/%Y")

    rows = []

    for i in range(total_installments):
        due_date = first_due_date + relativedelta(months=i)
        #formatted_due_date = due_date.strftime("%d/%m/%Y")
        real_due_date = due_date.date().isoformat()
        month_year = due_date.strftime("%m/%Y")
        installment_label = f"{str(i+1).zfill(2)}/{str(total_installments).zfill(2)}"

        rows.append({
            "Número do Documento": document_number,
            "Mês/Ano": month_year,
            "Fornecedor": supplier,
            "Descrição": description,
            "Valor (R$)": installment_value,
            "Data de Vencimento": real_due_date,
            "Data de Pagamento": "",
            "Forma de Pagamento": payment_method,
            "Situação": "Aberto",
            "Parcelas": installment_label,
            "Observações": notes
        })

    df = pd.DataFrame(rows)

    csv_path = "boletos.csv"
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        combined_df = df

    combined_df.to_csv(csv_path, index=False)
    print(f"\n✅ Boletos com Número do Documento {document_number} salvos em {csv_path}.")

    send_to_google_sheets(df)

if __name__ == "__main__":
    register_bills()
