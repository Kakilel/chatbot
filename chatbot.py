from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load model (can be changed to any chat model)
chatbot = pipeline("text-generation", model="gpt2")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = chatbot(user_input, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']
    return jsonify({"response": response})

history = []

def chat_with_memory(user_input):
    history.append(f"User: {user_input}")
    prompt = "\n".join(history) + "\nAI:"
    response = chatbot(prompt, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']
    history.append(f"AI: {response}")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
