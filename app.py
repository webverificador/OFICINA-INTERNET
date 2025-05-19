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
    <meta charset="utf-8">
    <title>Verificación de Certificados</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        .container {
            border: 1px solid #ddd;
            padding: 40px;
            width: 500px;
            margin: auto;
            border-radius: 10px;
            box-shadow: 2px 2px 12px #aaa;
        }
        input {
            margin: 10px;
            padding: 5px;
            width: 80%;
        }
        button {
            padding: 10px 20px;
        }
        iframe {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Verificación de Certificados</h2>
        <form method="POST">
            <label>Folio:</label><br>
            <input type="text" name="folio" placeholder="Ej: 500588087549" required><br>
            <label>Código de Verificación:</label><br>
            <input type="text" name="codigo" placeholder="Ej: 2d2d7b27e5c3" required><br>
            <button type="submit">Consultar</button>
        </form>
        {% if certificado %}
            <p style="margin-top: 20px; color: green;">Certificado encontrado:</p>
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
