from flask import Flask, jsonify, send_from_directory, request
import os
import subprocess
import shutil

app = Flask(__name__)

# Directorios de sincronización
PUBLIC_DIR = "/sync_files/public"
PRIVATE_DIR = "/sync_files/private"

@app.route('/')
def hello():
    return {'message': 'Synchrontainer está activo'}

@app.route('/despedirse')
def bye():
    return {'message': 'Adiós, mundo'}

@app.route('/storage/<uid>')
def list_files_from(uid):
    current_id = subprocess.check_output(['hostname']).decode().strip()
    if uid != current_id:
        return {'error': f'No puedes acceder al contenedor {uid}'}, 403

    return {
        'uid': current_id,
        'public': os.listdir(PUBLIC_DIR),
        'private': os.listdir(PRIVATE_DIR)
    }

@app.route('/public/')
def list_all_public():
    # Asume que todos los contenedores montan el mismo volumen compartido en /sync_files/public
    try:
        files = os.listdir(PUBLIC_DIR)
        return {'public_files': files}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(PUBLIC_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return {'error': 'Archivo no encontrado'}, 404

@app.route('/upload/<uid>/<filename>', methods=['POST'])
def upload_file(uid, filename):
    current_id = subprocess.check_output(['hostname']).decode().strip()
    if uid != current_id:
        return {'error': f'No puedes subir archivos a otro contenedor ({uid})'}, 403

    if 'file' not in request.files:
        return {'error': 'No se encontró ningún archivo en la petición'}, 400

    file = request.files['file']
    path = os.path.join(PUBLIC_DIR, filename)
    file.save(path)
    return {'message': f'Archivo {filename} subido correctamente'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
