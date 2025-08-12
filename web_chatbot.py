from flask import Flask, request, render_template_string, session
import random
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session

faq = {
    "python": "Python is a popular programming language known for its simplicity and versatility.",
    "install python": "You can download Python from python.org and follow the installation instructions for your OS.",
    "your name": "My name is GitHub Copilot.",
    "how are you": "I'm just code, but I'm here to help you!",
    "file not found": "Check your file path and make sure the file exists at the specified location.",
    "permission error": "Close any app using the file, pause OneDrive sync, or run your IDE as administrator.",
    "plot graph": "You can use matplotlib: import matplotlib.pyplot as plt; plt.plot([1,2,3],[4,5,6]); plt.show()",
    "read csv": "Use pandas: import pandas as pd; df = pd.read_csv('filename.csv')",
    "missing data": "Use pandas: df.dropna() to remove missing values or df.fillna(value) to fill them.",
    "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "nlp": "NLP stands for Natural Language Processing, a field of AI focused on understanding human language.",
    "weather": "Sorry, I can't provide weather updates.",
    "time": "The current time is " + datetime.datetime.now().strftime("%H:%M:%S") + "."
}

fallbacks = [
    "I'm not sure I understand, but I'm learning every day!",
    "Can you rephrase your question?",
    "Interesting! Tell me more.",
    "I don't have an answer for that, but you can ask me about Python, errors, or data analysis.",
    "Sorry, I don't know that yet. Try asking something else!"
]

def get_response(user_input):
    user_input = user_input.lower().strip()
    for key, answer in faq.items():
        if key in user_input:
            if key == "time":
                return "The current time is " + datetime.datetime.now().strftime("%H:%M:%S") + "."
            return answer
    if any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! 😊 How can I assist you today?"
    if any(word in user_input for word in ["bye", "exit", "quit", "goodbye"]):
        return "Goodbye! Have a wonderful day!"
    if "joke" in user_input:
        jokes = [
            "Why did the computer show up at work late? It had a hard drive!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the math book sad? Because it had too many problems."
        ]
        return random.choice(jokes)
    if "time" in user_input:
        return "The current time is " + datetime.datetime.now().strftime("%H:%M:%S") + "."
    if "thank" in user_input:
        return "You're welcome! 😊"
    if "help" in user_input:
        return "You can greet me, ask for a joke, the time, or just chat!"
    return random.choice(fallbacks)

HTML = """
<!doctype html>
<title>Creative Chatbot</title>
<h2>Rule-Based Chatbot</h2>
<form method=post>
  <input name=user_input autofocus autocomplete="off" style="width:300px;">
  <input type=submit value=Send>
</form>
{% if chat_history %}
  <h3>Conversation History:</h3>
  {% for chat in chat_history %}
    <p><b>You:</b> {{ chat[0] }}</p>
    <p><b>Chatbot:</b> {{ chat[1] }}</p>
    <hr>
  {% endfor %}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if "chat_history" not in session:
        session["chat_history"] = []
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
        session["chat_history"].append((user_input, response))
        session.modified = True
    return render_template_string(HTML, chat_history=session.get("chat_history", []))

if __name__ == "__main__":
    print("Chatbot running at http://localhost:5000")
    app.run(debug=True)