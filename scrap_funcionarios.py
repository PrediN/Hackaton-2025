from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By         
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


service = Service(r"C:\Program Files\chromedriver-win64\chromedriver.exe")


options = Options()
options.add_argument("--headless") 
driver = webdriver.Chrome(service=service, options=options)

url = "https://masander.github.io/AlimenticiaLTDA/#/humanresources"
driver.get(url)

def extrair_tabela():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    tabela = driver.find_element(By.TAG_NAME, "table")
    linhas = tabela.find_elements(By.TAG_NAME, "tr")

    dados = []
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if not colunas:  
            colunas = linha.find_elements(By.TAG_NAME, "th")
        dados.append([coluna.text.strip() for coluna in colunas])
    return dados

botao_funcionarios = driver.find_element(By.XPATH, "//button[contains(text(), 'Funcionários')]")
botao_funcionarios.click()

time.sleep(5) 

dados_funcionarios = extrair_tabela()

with pd.ExcelWriter("funcionarios.xlsx") as writer:
    pd.DataFrame(dados_funcionarios[1:], columns=dados_funcionarios[0]).to_excel(writer, sheet_name="Funcionarios", index=False)

print("Dados de Funcionários exportados com sucesso!")
driver.quit()
