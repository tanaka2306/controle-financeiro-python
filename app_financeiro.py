import sqlite3
from datetime import datetime

# FUNÇÃO 1: Cria o banco de dados CORRETO
def inicializar_sistema():
    conn = sqlite3.connect('meu_financeiro.db')
    cursor = conn.cursor()
    # Criamos a tabela já com a coluna TIPO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            descricao TEXT,
            valor REAL,
            categoria TEXT,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

# FUNÇÃO 2: Salva os dados (Entrada ou Saída)
def salvar_movimentacao(descricao, valor, categoria, tipo):
    try:
        conn = sqlite3.connect('meu_financeiro.db')
        cursor = conn.cursor()
        data_atual = datetime.now().strftime('%d/%m/%Y')
        
        cursor.execute('''
            INSERT INTO transacoes (data, descricao, valor, categoria, tipo)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_atual, descricao, abs(valor), categoria, tipo.upper()))
        
        conn.commit()
        conn.close()
        print(f"\n✅ {tipo} registrada com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao salvar: {e}")

# FUNÇÃO 3: Calcula o Saldo (Entradas - Saídas)
def exibir_extrato():
    conn = sqlite3.connect('meu_financeiro.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transacoes')
    dados = cursor.fetchall()
    
    total_entradas = 0
    total_saidas = 0

    print("\n" + "="*60)
    print(f"{'DATA':<12} | {'TIPO':<8} | {'DESCRIÇÃO':<15} | {'VALOR'}")
    print("-" * 60)

    for linha in dados:
        data, desc, valor, cat, tipo = linha[1], linha[2], linha[3], linha[4], linha[5]
        
        if tipo == 'ENTRADA':
            total_entradas += valor
        else:
            total_saidas += valor
            
        print(f"{data:<12} | {tipo:<8} | {desc:<15} | R$ {valor:>8.2f}")

    saldo_final = total_entradas - total_saidas
    print("-" * 60)
    print(f"TOTAL ENTRADAS: R$ {total_entradas:>8.2f}")
    print(f"TOTAL SAÍDAS:   R$ {total_saidas:>8.2f}")
    print(f"SALDO ATUAL:    R$ {saldo_final:>8.2f}  <--") 
    print("="*60)
    conn.close()

# --- INTERFACE ---
inicializar_sistema()

while True:
    print("\n1- Entrada | 2- Saída | 3- Ver Saldo | 4- Sair")
    op = input("Escolha: ")

    if op in ['1', '2']:
        tipo = "ENTRADA" if op == '1' else "SAIDA"
        desc = input(f"Descrição da {tipo}: ")
        try:
            val = float(input("Valor (R$): ").replace(',', '.'))
            cat = input("Categoria: ")
            salvar_movimentacao(desc, val, cat, tipo)
        except ValueError:
            print("\n❌ Erro: No valor, use apenas números e ponto!")
            
    elif op == '3':
        exibir_extrato()
    elif op == '4':
        print("Até logo, Lucas!")
        break