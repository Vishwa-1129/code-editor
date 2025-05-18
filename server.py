from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    user_input = data.get('input', '')

    with open('temp.py', 'w') as f:
        f.write(code)

    try:
        result = subprocess.run(
            ['python', 'temp.py'],
            input=user_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        output = result.stdout.decode() + result.stderr.decode()
    except subprocess.TimeoutExpired:
        output = 'Error: Code execution timed out.'

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

