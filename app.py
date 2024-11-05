from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATINS'] = False
db = SQLAlchemy(app)

class UserIMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

def create_db():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        if name and weight and height:
            try:
                weight = float(weight)
                height = float(height)

                imc = weight / (height ** 2)
                if imc < 18.5:
                    status = "Abaixo do peso"
                elif 18.5 <= imc <= 24.9:
                    status = "Peso normal"
                elif 25 <= imc <= 29.9:
                    status = "Sobrepeso"
                else:
                    status = "Obesidade"

                new_entry = UserIMC(name=name, weight=weight, height=height, imc=imc, status=status)
                db.session.add(new_entry)
                db.session.commit()

                return redirect(url_for('history'))
            except ValueError:
                print("Erro na conversão de peso ou altura.")
                return "Erro: Peso ou altura inválidos."
        else:
            print("Erro: Campos não preenchidos corretamente.")
            return "Erro: Campos não preenchidos corretamente."
    return render_template('index.html')

@app.route('/history')
def history():
    imc_records = UserIMC.query.all()
    return render_template('history.html', imc_records=imc_records)

if __name__ == '__main__':
    app.run(debug=True)