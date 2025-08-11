from flask import Flask, request, abort
import subprocess
import hmac
import hashlib
import os

app = Flask(__name__)

# Lee la clave secreta del entorno
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "cambia_esta_clave")
REPO_PATH = "/var/www/mi-sitio"  # Ruta a tu repo local
BRANCH = "main"  # Cambia a la rama que quieras

@app.route('/pull-repo', methods=['POST'])
def pull_repo():
    # 1. Validar firma de GitHub
    signature = request.headers.get("X-Hub-Signature-256")
    if signature is None:
        abort(403)

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        abort(403)

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        abort(403)

    # 2. Ejecutar actualización
    try:
        subprocess.run(["git", "-C", REPO_PATH, "fetch"], check=True)
        subprocess.run(["git", "-C", REPO_PATH, "reset", "--hard", f"origin/{BRANCH}"], check=True)

        # 3. Reiniciar servicio web (opcional)
        subprocess.run(["systemctl", "restart", "mi-sitio.service"], check=True)

        return "Actualización exitosa\n", 200
    except subprocess.CalledProcessError as e:
        return f"Error actualizando: {e}\n", 500

if __name__ == '__main__':
    app.run()

