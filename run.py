import os
from app import create_app, db
from flask_migrate import Migrate

# Убедитесь, что создаёте приложение через factory
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

# Инициализация миграций
migrate = Migrate(app, db)

# Переносим декоратор после инициализации приложения

@app.cli.command("run")
def run():
    app.run()

if __name__ == '__main__':
    app.run()