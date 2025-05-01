from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Initialize Groq client with API key from .env
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print(f"Received message: {data}")
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    try:
        # Send user's message to Groq LLM
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            model="llama3-70b-8192"
        )

        # Extract reply
        reply = chat_completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
