from projetosenac import app, database

# Roda isso UMA vez para criar o banco de dados
with app.app_context():
    database.create_all()
    print("Banco de dados criado com sucesso!")
