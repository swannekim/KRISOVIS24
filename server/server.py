from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

# app instance
app = Flask(__name__)
CORS(app) # allows port 8080 in use

# app routing @ /api/home
# python3 server.py : "Hello World!" will appear on http://127.0.0.1:8080/api/home
@app.route("/api/home", methods={'GET'})
def return_home():
    return jsonify({
        'testmessage': "Hello World!",
        'titleofweb': "KRISO 2024 Visualization",
        'shiptype': ['cargo', 'passenger', 'tanker', 'government']
    })

@app.route("/test", methods={'GET'})
def test():
    return jsonify({
        'testmessage': "Hello World!",
        'titleofweb': "KRISO 2024 Visualization",
        'shiptype': ['cargo', 'passenger', 'tanker', 'government']
    })

# app running
if __name__ == "__main__":
    app.run(debug=True, port=8080) # dev mode
    # app.run() # deploy production mode