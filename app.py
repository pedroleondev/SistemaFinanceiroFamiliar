from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # Campo para diferenciar Receita e Despesa


with app.app_context():
    db.create_all()

# ✅ ROTA PARA A PÁGINA INICIAL
@app.route('/')
def home():
    return render_template('index.html')

# ✅ ROTA PARA A PÁGINA DE LANÇAMENTOS
@app.route('/lancamentos')
def lancamentos():
    return render_template('lancamentos.html')

# ✅ ROTA PARA ADICIONAR NOVA DESPESA
@app.route('/nova-despesa')
def nova_despesa():
    return render_template('nova_despesa.html')

# ✅ ROTA PARA ADICIONAR NOVA RECEITA
@app.route('/nova-receita')
def nova_receita():
    return render_template('nova_receita.html')

# ✅ ROTA PARA SOMAR TOTAIS DE DESPESAS/RECEITAS
@app.route('/totais', methods=['GET'])
def get_totais():
    receita_total = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Receita').scalar() or 0.0
    despesa_total = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Despesa').scalar() or 0.0
    saldo_geral = receita_total + despesa_total  # Como despesas são negativas, a soma já é correta

    return jsonify({
        "receita_mensal": f"R$ {receita_total:.2f}",
        "despesa_mensal": f"R$ {abs(despesa_total):.2f}",  # Exibe o valor absoluto para ficar positivo
        "saldo_geral": f"R$ {saldo_geral:.2f}"
    })


# ✅ API PARA OBTER TRANSAÇÕES (JÁ EXISTIA)
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{'id': t.id, 'description': t.description, 'amount': t.amount, 'date': t.date, 'category': t.category} for t in transactions])

# ✅ API PARA ADICIONAR TRANSAÇÃO (JÁ EXISTIA)
@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        date=data['date'],
        category=data['category'],
        type=data.get('type', "Receita")  # Padrão será "Receita" se não for enviado
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
