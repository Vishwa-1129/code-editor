from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import uuid
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend is running!"

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
