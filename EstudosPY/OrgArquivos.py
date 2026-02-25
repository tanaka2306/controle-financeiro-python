import os
import shutil
from datetime import datetime

# 1. Definir o caminho da pasta de Downloads de forma automática
caminho_downloads = os.path.expanduser("~/Downloads")

# 2. Dicionário para converter o número do mês no nome da pasta
meses_nomes = {
    1: "01_Janeiro", 2: "02_Fevereiro", 3: "03_Março", 4: "04_Abril",
    5: "05_Maio", 6: "06_Junho", 7: "07_Julho", 8: "08_Agosto",
    9: "09_Setembro", 10: "10_Outubro", 11: "11_Novembro", 12: "12_Dezembro"
}

def organizar_arquivos():
    # 3. Listar tudo o que tem na pasta
    for arquivo in os.listdir(caminho_downloads):
        
        # Corrigido: os.path.join (com 'h' no final)
        caminho_completo = os.path.join(caminho_downloads, arquivo)
        
        # 4. Verificar se é um arquivo (ignora pastas)
        if os.path.isfile(caminho_completo):
            
            # Pegar a data de modificação
            timestamp = os.path.getmtime(caminho_completo)
            data_do_arquivo = datetime.fromtimestamp(timestamp)
            
            # Identificar o mês e o nome da pasta destino
            numero_mes = data_do_arquivo.month
            nome_da_pasta = meses_nomes[numero_mes]
            caminho_destino_pasta = os.path.join(caminho_downloads, nome_da_pasta)
            
            # 5. Criar a pasta se não existir
            if not os.path.exists(caminho_destino_pasta):
                os.makedirs(caminho_destino_pasta)
            
            # 6. Mover o arquivo
            try:
                shutil.move(caminho_completo, os.path.join(caminho_destino_pasta, arquivo))
                print(f"Movido: {arquivo} -> {nome_da_pasta}")
            except Exception as e:
                print(f"Erro ao mover {arquivo}: {e}")

if __name__ == "__main__":
    organizar_arquivos()
    print("\nOrganização finalizada com sucesso!")