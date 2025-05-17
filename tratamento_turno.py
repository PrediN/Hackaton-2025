import pandas as pd

df_freq = pd.read_excel("funcionarios_atual.xlsx")

df_freq = pd.DataFrame(df_freq)

for row, linha in df_freq.iterrows():
    match df_freq.at[row, "Turno"]:
        case("Manhã"): 
            print("Horário de Trabalho 06:00 até 14:00")
            df_freq.at[row,"Entrada"] = "06:00"
            df_freq.at[row,"Saída"] = "14:00"
        case("Tarde"): 
            print("Horário de Trabalho 14:00 até 22:00")
            df_freq.at[row,"Entrada"] = "14:00"
            df_freq.at[row,"Saída"] = "22:00"
        case("Noite"): 
            print("Horário de Trabalho 22:00 até 06:00")
            df_freq.at[row,"Entrada"] = "22:00"
            df_freq.at[row,"Saída"] = "06:00"

df_freq.to_excel('funcionarios_corrigido.xlsx', index=False)
