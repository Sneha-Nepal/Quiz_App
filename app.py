import time
import score_manager
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from data import fetch_questions
from question_model import Question

app = Flask(__name__)
app.secret_key = "super_secret_quiz_key"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form.get("user_name").strip().capitalize()
        session["user_name"] = user_name
        session["question_number"] = 0
        session["score"] = 0
        session["questions"] = fetch_questions(amount=5)
        return redirect(url_for("quiz"))

    return render_template("index.html")

@app.route("/result")  # <-- Endpoint name is 'result' based on function name below
def result():
    user_name = session.get("user_name")
    final_score = session.get("score", 0)

    is_new_record, old_score = score_manager.update_user_score(
        user_name, final_score
    )

    leaderboard_data = score_manager.get_leaderboard() or []
    
    return render_template(
        "result.html",
        user_name=user_name,
        score=final_score,
        is_new_record=is_new_record,
        old_score=old_score,
        leaderboard =leaderboard_data,
    )


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    user_name = session.get("user_name")
    raw_questions = session.get("questions", [])

    if not user_name or not raw_questions:
        return redirect(url_for("index"))

    questions = [
        Question(q["text"], q["answer"], q["options"]) for q in raw_questions
    ]
    q_index = session.get("question_number", 0)

    if q_index >= len(questions):
        return redirect(url_for("result"))

    current_q = questions[q_index]

    if request.method == "POST":
        selected_option = request.form.get("option")

        # 1. Calculate time taken
        start_time = session.get("start_time", time.time())
        elapsed_time = round(time.time() - start_time, 1)

        # 2. Check answer and assign bonus points
        if selected_option == current_q.answer:
            if elapsed_time <= 10:
                session["score"] += 2
                feedback = f"⚡ Fast answer! You took {elapsed_time}s and earned +2 points!"
            else:
                session["score"] += 1
                feedback = (
                    f" Correct! You took {elapsed_time}s and earned +1 point."
                )
        else:
            feedback = f"❌ Wrong! The correct answer was: {current_q.answer}"

        session["question_number"] += 1
        session["feedback"] = feedback  # Store feedback for display
        return redirect(url_for("quiz"))

    # Track time when user GETs the page
    session["start_time"] = time.time()

    # Retrieve and clear feedback for the current view
    feedback = session.pop("feedback", None)

    return render_template(
        "quiz.html",
        question=current_q,
        q_num=q_index + 1,
        total=len(questions),
        current_score=session.get("score", 0),
        feedback=feedback,
    )

if __name__ == "__main__":
    app.run(debug=True)
