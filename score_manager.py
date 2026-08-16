import csv

FILENAME = "high_scores.csv"

def load_scores():
    """Reads CSV and returns a dictionary containing user names to their high score."""
    scores = {}
    try:
        with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)                                       # Each row looks like : {"name": "...", "high_score": "..."}
            for row in reader:
                if row and row.get("name"):                                     # Check not empty and has name value
                    scores[row["name"].strip()] = int(row["high_score"])
    except FileNotFoundError:
        print("File doesn't exist")

    return scores


def save_scores(scores):
    """Writes the dictionary of scores back to the CSV file."""
    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "high_score"])                                  # Writing the column header
        # Loops through the dictionary and writes the name and high_score in csv file
        for name, high_score in scores.items():             
            writer.writerow([name, high_score])


# Not used in app.py
def get_user_highscore(name):
    """Returns previous high score for a given name or None if new user."""
    scores = load_scores()
    return scores.get(name)


def update_user_score(name, new_score):
    """Updates score by returning (is_new_high_score, previous_high_score)."""
    scores = load_scores()
    prev_score = scores.get(name)

    if prev_score is None or new_score > prev_score:
        scores[name] = new_score
        save_scores(scores)
        return True, prev_score

    return False, prev_score


def get_leaderboard():
    scores = []
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)                                          # Skips the header for iteration below
            for row in reader:
                if row:                                                 # If row not empty
                    name, score = row[0], int(row[1])
                    scores.append({"name": name, "score": score})

        # Sort highest to lowest scores
        scores.sort(key=lambda x: x["score"], reverse=True)

        return scores                                                   # Returns the sorted list

    except FileNotFoundError:
        return []
    