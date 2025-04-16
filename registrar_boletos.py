import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

def gerar_parcelas():
    fornecedor = input("Fornecedor: ")
    descricao = input("Descrição: ")
    valor_total = float(input("Valor total (ex: 900.00): "))
    num_parcelas = int(input("Número de parcelas: "))
    vencimento_inicial = input("Data do 1º vencimento (formato YYYY-MM-DD): ")
    forma_pagamento = input("Forma de pagamento (ex: Boleto, Pix): ")

    vencimento_base = datetime.strptime(vencimento_inicial, "%Y-%m-%d")
    valor_parcela = round(valor_total / num_parcelas, 2)
    
    dados = []

    for i in range(num_parcelas):
        vencimento = vencimento_base + relativedelta(months=i)
        parcela_formatada = f"{str(i+1).zfill(2)}/{str(num_parcelas).zfill(2)}"
        mes_ano = vencimento.strftime("%m/%Y")
        
        dados.append({
            "Mês/Ano": mes_ano,
            "Fornecedor": fornecedor,
            "Descrição": descricao,
            "Valor (R$)": valor_parcela,
            "Data de Vencimento": vencimento.strftime("%d/%m/%Y"),
            "Data de Pagamento": "",
            "Forma de Pagamento": forma_pagamento,
            "Situação": "Aberto",
            "Parcelas": parcela_formatada,
            "Observações": ""
        })

    return pd.DataFrame(dados)

def salvar_em_excel(df, caminho_arquivo="boletos.xlsx"):
    if os.path.exists(caminho_arquivo):
        df_existente = pd.read_excel(caminho_arquivo)
        df_final = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_final = df
    df_final.to_excel(caminho_arquivo, index=False)
    print(f"\n✅ Boletos salvos em: {caminho_arquivo}")

# --- Execução principal ---
if __name__ == "__main__":
    df_novo = gerar_parcelas()
    salvar_em_excel(df_novo)
