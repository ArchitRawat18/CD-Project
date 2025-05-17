from flask import Flask, request, jsonify
from lexer import tokenize
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/lexer', methods=['POST'])
def run_lexer():
    data = request.get_json()
    code = data.get("code", "")
    tokens = tokenize(code)
    return jsonify({"tokens": tokens})

@app.route('/parser', methods=['POST'])
def run_parser():
    tokens = request.json.get('tokens', [])

    try:
        tokens_json = json.dumps(tokens)
        result = subprocess.run(
            ['java', '-cp', '.;lib/json-20250107.jar', 'parser'],  # Adjust classpath as needed
            input=tokens_json.encode(),
            capture_output=True,
            timeout=5
        )

        output = result.stdout.decode().strip()

        if result.returncode != 0 or not output:
            return jsonify({'error': 'Parser failed', 'stderr': result.stderr, 'raw_output': output}), 500

        # Try to parse the output as JSON
        try:
            parsed_output = json.loads(output)
            if "error" in parsed_output:
                return jsonify({'error': parsed_output["error"], 'raw_output': output}), 400
            return jsonify({"parse_tree": parsed_output})
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON output from parser', 'raw_output': output}), 500


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
