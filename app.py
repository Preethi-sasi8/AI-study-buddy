
from flask import Flask, render_template, request, session
from agents import run_explainer, run_quiz, run_flashcards

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form["topic"]
        session["topic"] = topic   # 🔥 store topic
        result = run_explainer(topic)
        return render_template("index.html", response=result)

    return render_template("index.html")

@app.route("/quiz")
def quiz():
    topic = session.get("topic")

    if not topic:
        return "Please enter a topic on the home page first."

    result = run_quiz(topic)
    return render_template("quiz.html", response=result)
@app.route("/flashcards")
def flashcards():
    topic = session.get("topic")

    if not topic:
        return "Please enter a topic on the home page first."

    result = run_flashcards(topic)
    return render_template("flashcards.html", response=result)


if __name__ == "__main__":
    app.run(debug=True)