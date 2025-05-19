
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__)
CERT_DIR = "certificados"

@app.route("/", methods=["GET", "POST"])
def index():
    certificado = None
    if request.method == "POST":
        folio = request.form["folio"]
        codigo = request.form["codigo"]
        df = pd.read_csv("certificados.csv")
        match = df[(df["folio"] == folio) & (df["codigo"] == codigo)]
        if not match.empty:
            certificado = match.iloc[0]["nombre_archivo"]
    return render_template("index.html", certificado=certificado)

@app.route("/ver/<path:filename>")
def ver_pdf(filename):
    return send_from_directory(CERT_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
