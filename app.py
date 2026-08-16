import time
import score_manager
from flask import (
    Flask,
    redirect,           # Send the browser to different URL
    render_template,    # Renders the HTML files from templates/       
    request,            # Gives access to incoming data
    session,            # Dictionary like object
    url_for,            # Generates URL from a fucntion name
)
from data import fetch_questions
from question_model import Question

app = Flask(__name__)           # Creates a flask object. __name__ tells the where to look for templetes files
app.secret_key = "super_secret_quiz_key"        # Usually hidden but fine here for now


@app.route("/", methods=["GET", "POST"])        # GET =  view, POST = submit the form
def index():
    """When the form is submitted, gets the user name from the root URL(/) or renders index.html"""
    if request.method == "POST":
        user_name = request.form.get("user_name").strip().capitalize()

        # Storing into the session cokkie
        session["user_name"] = user_name
        session["question_number"] = 0
        session["score"] = 0

        session["questions"] = fetch_questions(amount=5)            # 5 requests from API
        return redirect(url_for("quiz"))            # Redirect the browser to (/quiz)

    return render_template("index.html")            # If not POST then GET the index.html


@app.route("/result")  # Endpoint name is 'result' based on function name below
def result():
    """Gets the name and final score"""
    user_name = session.get("user_name")
    final_score = session.get("score", 0)           # Setting default final score to 0 if none

    # is_new_score is boolean and old_score is the previous_score. Comparing betweeen two scores
    is_new_record, old_score = score_manager.update_user_score(user_name, final_score)

    # Gets the leaderboard data. If leaderboard returns None then default is an empty list
    leaderboard_data = score_manager.get_leaderboard() or []

    # Gets result.html file by passing all the variables like user_name, score, ...
    return render_template(
        "result.html",
        user_name=user_name,
        score=final_score,
        is_new_record=is_new_record,
        old_score=old_score,
        leaderboard=leaderboard_data,
    )


# Main game loop
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    user_name = session.get("user_name")
    raw_questions = session.get("questions", [])

    # If user_name or question is empty return index.html
    if not user_name or not raw_questions:
        return redirect(url_for("index"))

    # Converts the raw disctionary into question object
    questions = [
        Question(q["text"], q["answer"], q["options"]) for q in raw_questions
    ]

    # Gets the current question index
    q_index = session.get("question_number", 0)
    if q_index >= len(questions):
        return redirect(url_for("result"))      # If the current question is last then show result
    current_q = questions[q_index]              # Gets the current question

    # Get the answer option of user click. This is the POST block
    if request.method == "POST":
        selected_option = request.form.get("option")

        # Calculates time between question launch and user answer
        start_time = session.get("start_time", time.time())
        elapsed_time = round(time.time() - start_time, 1)

        # Check answers and assign points
        if selected_option == current_q.answer:
            if elapsed_time <= 10:
                session["score"] += 2
                feedback = f"⚡ Fast answer! You took {elapsed_time}s and earned +2 points!"
            else:
                session["score"] += 1
                feedback = (f" Correct! You took {elapsed_time}s and earned +1 point.")
        else:
            feedback = f"❌ Wrong! The correct answer was: {current_q.answer}"

        # Moves to next question, gives feedback, and redirects to the quiz page for looping the process
        session["question_number"] += 1
        session["feedback"] = feedback  
        return redirect(url_for("quiz"))        # New request

    # Track time when user GETs the quesion i.e. the start_time
    session["start_time"] = time.time()

    # Retrieve and clear feedback for the current view
    feedback = session.pop("feedback", None)

    # Renders the question page with the following variables
    return render_template(
        "quiz.html",
        question=current_q,
        q_num=q_index + 1,
        total=len(questions),
        current_score=session.get("score", 0),
        feedback=feedback,
    )

# Run the server if this file is executed directly as in 'python app.py'
if __name__ == "__main__":
    app.run(debug=True)
