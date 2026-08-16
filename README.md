# Quiz Game

Quiz_App is a Python-based application that fetches questions from an external API (`OpenTDB`), tracks player scores in a CSV file, and utilizes Object-Oriented Programming (OOP) principles like encapsulation and inheritance. It utilizes Python's `Flask` framework for web-based platform.
I was assisted with AI, then went through it line by line until I actually understood how every part works

## Features

* **Live Trivia Questions:** Fetches 5 fresh multiple-choice questions from the OpenTDB API every time a new quiz starts.
* **Timed Scoring:** Answering correctly within 10 seconds earns +2 points, answering correctly but slower earns +1 point, and no points for wrong answer.
* **Session-Based Game State:** Uses Flask's `session` to track the player's name, current question, running score, and question data across separate HTTP requests, without needing a database.
* **Persistent High Scores:** Every completed quiz is checked against the player's personal best and saved to a CSV file, so return players can try to beat their own record.
* **Leaderboard:** Displays every player's best score, ranked highest to lowest, on the results page.

## Concepts Learned & Applied

### Flask
 
* Set up routes for the home page, quiz loop, and results page using `@app.route()`.
* Used `request.method` to handle both GET (showing a page) and POST (submitting a form) on the same URL.
* Learned how a signed session cookie lets a stateless server "remember" a player between requests — name, score, question progress, and even the questions themselves all live in the session rather than server memory.
* Used the **Post/Redirect/Get Pattern**to redirect after every submitted answer instead of rendering directly. So, refreshing the page never resubmits the same answer twice.

### Requests Library
 
* Used `requests.get()` to call the OpenTDB API and pull down live trivia questions.
* Checked `response.status_code` to catch failed requests before trying to process the response.
* Parsed the returned JSON with `response.json()` to get usable Python data.
* Wrapped the API call in a `try/except` block to catch network errors (`requests.RequestException`) without crashing the app.

### OOP
 
* Wrapped each raw question dictionary from the API into a `Question` class (`question.text`, `question.answer`, `question.options`) instead of juggling raw dicts everywhere.
* Used encapsulation to keep a question's data and behavior bundled together in one object.
* Kept the class simple and reusable — the same `Question` object works whether it came from a fresh API call or session-stored data.

### API
 
* Learned how a REST API like OpenTDB returns structured JSON data in response to a URL request with query parameters (`amount`, `category`, `difficulty`, `type`).
* Cleaned up the response with `html.unescape()` to fix HTML-encoded characters (like `&#039;`) before displaying questions.
* Understood the difference between an HTTP-level failure (bad status code) and an API-level failure (valid response, but no results).
* Learned to treat API calls as unreliable by nature and always planning for empty results or network failures rather than assuming a clean response every time.

### File I/O with CSV
 
Used Python's `csv` module to read and write a `high_scores.csv` file, handling first-time players, updated records, and building a sorted leaderboard from it.
 
### Jinja Templating
 
Used `{% if %}`, `{% for %}`, and `url_for()` inside HTML templates to render dynamic content — like the current question, live feedback, and the leaderboard table — without hardcoding anything.
