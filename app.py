from Flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Inicialização do banco de dados
def init_db():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Categoria TEXT NOT NULL,
                TemIrmao INTEGER,
                ID_Irmao INTEGER
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Missas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Horario TEXT NOT NULL,
                Data TEXT NOT NULL
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Disponibilidades (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UsuarioID INTEGER,
                MissaID INTEGER,
                FOREIGN KEY (UsuarioID) REFERENCES Usuarios(ID),
                FOREIGN KEY (MissaID) REFERENCES Missas(ID)
            );
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    categoria = request.form['categoria']
    tem_irmao = 1 if 'tem_irmao' in request.form else 0
    id_irmao = request.form.get('id_irmao')

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Nome, Categoria, TemIrmao, ID_Irmao) VALUES (?, ?, ?, ?)",
                       (nome, categoria, tem_irmao, id_irmao))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/cadastrar_missa', methods=['POST'])
def cadastrar_missa():
    horario = request.form['horario']
    data = request.form['data']

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Missas (Horario, Data) VALUES (?, ?)", (horario, data))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/distribuir_missas')
def distribuir_missas():
    # Algoritmo de distribuição aqui
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
