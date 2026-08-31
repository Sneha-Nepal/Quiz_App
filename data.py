import html
import random
import requests


def fetch_questions(amount=10, category=18, difficulty="easy"):
    """Fetches MCQ questions from OpenTDB API and formats them as standard dictionaries."""
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching questions: {response.status_code}")
            return []

        # Converts JSON response to python dictionary
        data = response.json()
        raw_results = data.get("results", [])               # Pulls out the list of questions

        formatted_questions = []
        for item in raw_results:
            # Unescape HTML entities in text and choices. Example : "What&#039;s the capital?" are converted back to "What's the capital?"
            question_text = html.unescape(item["question"])
            correct_ans = html.unescape(item["correct_answer"])
            incorrect_ans = [html.unescape(ans) for ans in item["incorrect_answers"]]

            # Store options as a list and shuffles them
            options = incorrect_ans + [correct_ans]
            random.shuffle(options)

            formatted_questions.append(
                {
                    "text": question_text,
                    "answer": correct_ans,
                    "options": options,
                }
            )

        return formatted_questions

    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []
