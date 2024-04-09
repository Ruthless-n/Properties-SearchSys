# Flask import
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def connect_db():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('imoveis.db')
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Rota para processar a busca
@app.route('/search', methods=['POST'])
def search():
    try:
        # Obtém o termo de busca do formulário
        termo = request.form['termo']

        # Conecta-se ao banco de dados
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            # Construir a consulta SQL dinamicamente
            query = f"SELECT DISTINCT {termo} FROM imoveis"

            # Executa a consulta SQL
            cursor.execute(query)
            results = cursor.fetchall()

            # Fechar a conexão com o banco de dados
            conn.close()

            # Renderizar a página de resultados com os dados encontrados
            return render_template('index.html', results=results)
        else:
            # Se a conexão com o banco de dados falhar, redirecionar para a página principal
            return redirect(url_for('index'))
    except Exception as e:
        print("Erro durante a busca:", e)
        # Em caso de erro, redirecionar para a página principal
        return redirect(url_for('index'))

# Rota principal para exibir a página de busca
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Executar o aplicativo Flask
    app.run(debug=True)
