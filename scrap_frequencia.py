from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time

URL = "https://masander.github.io/AlimenticiaLTDA/#/humanresources"

options = Options()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

def extrair_despesas():
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    dados = []

    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) < 6:
            continue

        id_funcionario = colunas[0].text.strip()
        timestamp = colunas[1].text.strip()
        entrada = colunas[2].text.strip()
        saida = colunas[3].text.strip()
        falta = colunas[4].text.strip()
        horas_extras = colunas[5].text.strip()

        try:
            data = datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")
        except:
            data = ""

        dados.append({
            "Id_funcionario": id_funcionario,
            "Data": data,
            "Entrada": entrada,
            "Saida": saida,
            "Falta": falta if falta else None,
            "Horas_extras": horas_extras
        })
        print(f"Adquirindo dados da linha: {linha}")

    return pd.DataFrame(dados)

try:
    driver.get(URL)

    print("🔍 Extraindo Frequencia...")
    df_despesas = extrair_despesas()
    df_despesas.to_excel("despesas.xslx", index=False)

finally:
    driver.quit()
