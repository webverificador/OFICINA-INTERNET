from flask import Flask, render_template_string, request, send_from_directory
import csv
import os

app = Flask(__name__)
CERT_DIR = "certificados"

@app.route("/", methods=["GET", "POST"])
def index():
    certificado = None
    if request.method == "POST":
        folio = request.form["folio"]
        codigo = request.form["codigo"]
        with open("certificados.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["folio"] == folio and row["codigo"] == codigo:
                    certificado = row["nombre_archivo"]
                    break
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Verificación de Certificados</title>
</head>
<body>
<div style="text-align: center;">
    <h2>Verificación de Certificados</h2>
    <form method="POST">
        <label>Folio:</label>
        <input type="text" name="folio" required><br>
        <label>Código de Verificación:</label>
        <input type="text" name="codigo" required><br>
        <button type="submit">Consultar</button>
    </form>
    {% if certificado %}
    <p style="color: green;">Certificado encontrado:</p>
    <iframe src="/ver/{{ certificado }}" width="100%" height="500px"></iframe>
    {% endif %}
</div>
</body>
</html>
""", certificado=certificado)

@app.route("/ver/<path:filename>")
def ver_pdf(filename):
    return send_from_directory(CERT_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
