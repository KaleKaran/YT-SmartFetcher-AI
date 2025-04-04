from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/data')
def get_data():
    return jsonify({
        "success": True,
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    })

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    # Process the data here (in a real app)
    return jsonify({"success": True, "received": data})

if __name__ == '__main__':
    app.run(debug=True)
