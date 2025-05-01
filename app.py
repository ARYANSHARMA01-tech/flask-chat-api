from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import threading
import time
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def periodic_request():
    while True:
        try:
            requests.get("https://your-app.onrender.com/ping")
            time.sleep(14 * 60)
        except Exception as e:
            print("Keep-alive failed:", e)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Message is required."}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            model="llama3-70b-8192"
        )
        return jsonify({"response": chat_completion.choices[0].message.content})  # Key changed

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route("/ping")
def ping():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    threading.Thread(target=periodic_request, daemon=True).start()
    app.run()