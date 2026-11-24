import os

from flask import Flask

import db
from modules import auth, usuarios, vehiculos

app = Flask(__name__)
# Clave para firmar la sesión. En producción define la variable SECRET_KEY.
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(usuarios.bp)
app.register_blueprint(vehiculos.bp)

if __name__ == "__main__":
    app.run(debug=True)
