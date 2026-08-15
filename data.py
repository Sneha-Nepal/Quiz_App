import html
import random
import requests


def fetch_questions(amount=10, category=18, difficulty="medium"):
    """Fetches MCQ questions from OpenTDB API and formats them as standard dicts."""
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching questions: {response.status_code}")
            return []

        data = response.json()
        raw_results = data.get("results", [])

        formatted_questions = []
        for item in raw_results:
            # Unescape HTML entities in text and choices
            question_text = html.unescape(item["question"])
            correct_ans = html.unescape(item["correct_answer"])
            incorrect_ans = [
                html.unescape(ans) for ans in item["incorrect_answers"]
            ]

            # Store options as a list
            options = incorrect_ans + [correct_ans]

            # ADDED: Shuffle options so the correct answer isn't always last
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


# ADDED: Interactive Game Loop
if __name__ == "__main__":
    print("Fetching trivia questions...\n")
    question_data = fetch_questions(amount=5)

    if not question_data:
        print("No questions loaded. Exiting.")
        exit()

    score = 0

    for idx, q in enumerate(question_data, start=1):
        print(f"Question {idx}: {q['text']}")

        # Print options as 1, 2, 3, 4
        for opt_idx, option in enumerate(q["options"], start=1):
            print(f"  {opt_idx}. {option}")

        # Get user answer
        try:
            choice = int(input("\nYour answer (1-4): ")) - 1
            selected_option = q["options"][choice]

            if selected_option == q["answer"]:
                print(" Correct!\n")
                score += 1
            else:
                print(f" Wrong! The correct answer was: {q['answer']}\n")
        except (ValueError, IndexError):
            print(
                f" Invalid input! The correct answer was: {q['answer']}\n"
            )

    print("=" * 30)
    print(f"Game Over! Final Score: {score}/{len(question_data)}")
    