import os
from app import db, app

db_path = "finance.db"

# Remove o banco se existir (para forçar a criação)
if os.path.exists(db_path):
    os.remove(db_path)
    print("Banco antigo removido.")

# Agora cria um novo banco
with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
