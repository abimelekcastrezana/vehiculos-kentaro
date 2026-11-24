from flask import Flask

import db
from modules import auth, usuarios, vehiculos

app = Flask(__name__)
app.secret_key = "contrasena" 

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(usuarios.bp)
app.register_blueprint(vehiculos.bp)

if __name__ == "__main__":
    app.run(debug=True)
