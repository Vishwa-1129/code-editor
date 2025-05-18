from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import uuid
from flask_cors import CORS

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code')
    user_input = data.get('input', '')

    filename = f'temp_{uuid.uuid4().hex}.py'
    with open(filename, 'w') as f:
        f.write(code)

    try:
        result = subprocess.run(
            ['python', filename],
            input=user_input,
            text=True,
            capture_output=True,
            timeout=5
        )
        output = result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        output = "Execution timed out"
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        os.remove(filename)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
