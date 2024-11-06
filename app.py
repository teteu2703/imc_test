from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        status = "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        status = "Peso normal"
    else:
        status = "Acima do peso"
    return imc, status

def init_db():
    conn = sqlite3.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT,
                    peso REAL,
                    altura REAL,
                    imc REAL,
                    status TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc, status = calcular_imc(peso, altura)

        conn = sqlite3.content('imc_db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO dados (nome, peso, altura, imc, status) VALUES (?, ?,?, ?, ?)',
                        (nome, peso, altura, imc, status))
        conn.commit()
        conn.close()

        return redirect(url_for('resultados'))
    
    return render_template('index.html')

@app.route('/resultados')
def resultados():
    conn = sqlite3.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, peso, altura, imc, status FROM dados')
    registros = cursor.fetchall()
    conn.close()

    return render_template('resultados.html', registros=registros)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)