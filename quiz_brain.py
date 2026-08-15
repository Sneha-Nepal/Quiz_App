import random
import time


class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    def still_has_questions(self):
        """Checks if questions are left in the question_bank."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Displays question with MCQ choices A/B/C/D and checks timing."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        # Shuffle options once per question display
        options = current_question.options.copy()
        random.shuffle(options)

        # Map 'A', 'B', 'C', 'D' to the corresponding option text
        labels = ["A", "B", "C", "D"]
        option_map = {
            labels[i]: options[i] for i in range(len(options))
        }

        print(f"\nQ.{self.question_number}: {current_question.text}")
        for label, text in option_map.items():
            print(f"  {label}) {text}")

        start_time = time.time()
        user_choice = (
            input("\nYour choice (A/B/C/D): ").strip().upper()
        )
        end_time = time.time()

        elapsed = round(end_time - start_time, 1)

        # Get actual text picked by user (or default to empty if invalid input)
        selected_text = option_map.get(user_choice, "")

        self.check_answer(selected_text, current_question.answer, elapsed)

    def check_answer(self, user_answer, correct_answer, e_time):
        """Checks the answer, tracks time bonus, and updates score."""
        print(f"You took {e_time} seconds.")

        if user_answer.lower() == correct_answer.lower():
            if e_time <= 10:
                print(
                    "Correct! Answered in under 10s -> +2 Points!"
                )
                self.score += 2
            else:
                print("Correct! -> +1 Point.")
                self.score += 1
        else:
            print(f"Wrong answer! The correct answer was: {correct_answer}")

        print(
            f"Current Score: {self.score} | Question {self.question_number}/{len(self.question_list)}"
        )
        print("-" * 40)
