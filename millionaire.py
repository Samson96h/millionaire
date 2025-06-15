import argparse
from random import randint, shuffle

QUESTIONS_COUNT = 5

parser = argparse.ArgumentParser(description="MILLIONAIRE")
parser.add_argument("-f", "--file", default="questions.txt", help="Question file")
parser.add_argument("-n", "--name", help="User name")
parser.add_argument("-t", "--top", default="top.txt", help="Top players")
parser.add_argument("-y", "--yes", type=str, help="See top players - y or n")
args = parser.parse_args()

yes = args.yes
QUESTIONS_FILE = args.file
USERNAME = args.name
TOP = args.top

def main():
    answer = input("Do you want to play or add questions? (play / edit): ").strip().lower()
    if answer == "play":
        game()
    elif answer == "edit":
        password = input("Enter password: ").strip()
        if password == "admin":
            edit()
        else:
            print("Incorrect password.")
    else:
        print("Unknown command. Please enter 'play' or 'edit'.")

def edit():
    new_question = input("Enter a new question: ").strip()
    if not new_question.endswith("?"):
        new_question += "?"

    answer_input = input("Enter 4 answers (first is correct), separated by commas: ").strip()
    answers = [a.strip() for a in answer_input.split(",")]

    if len(answers) != 4:
        print("You must enter exactly 4 answers (1 correct and 3 incorrect).")
        return

    question_line = new_question + ",".join(answers)

    try:
        with open(QUESTIONS_FILE, "a", encoding="utf-8") as f:
            f.write(question_line + "\n")
        print("Question added successfully.")
    except Exception as e:
        print("Error saving question:", e)

def get_questions(fname):
    try:
        with open(fname, encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if "?" in line]
    except FileNotFoundError:
        print(f"File {fname} not found. Questions not loaded.")
        return []

def get_random_indexes(qcount, count):
    indexes = set()
    while len(indexes) < count:
        indexes.add(randint(0, qcount - 1))
    return list(indexes)

def prepare_questions(questions):
    final = []
    for q in questions:
        if "?" in q:
            q_text, ans_text = q.split("?", 1)
            q_text += "?"
            answers = [a.strip() for a in ans_text.split(",")]
            if len(answers) < 4:
                continue
            correct = answers[0]
            shuffle(answers)
            final.append({
                "question": q_text,
                "variants": answers,
                "correct": correct
            })
    return final

def play_quiz(questions):
    score = 0
    for q in questions:
        print("\n" + q["question"])
        for i, a in enumerate(q["variants"], 1):
            print(f"{i}. {a}")

        try:
            choice = input("Your answer (1-4): ").strip()
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= 4:
                    answer = q["variants"][num - 1]
                else:
                    print("Number must be from 1 to 4.")
                    answer = ""
            else:
                print("Enter a number.")
                answer = ""
        except Exception as e:
            print("Input error:", e)
            answer = ""

        if answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            if answer != "":
                print(f"Incorrect! Correct answer: {q['correct']}")
    return score

def save_score(fname, username, score):
    if not username:
        username = input("Enter your name: ").strip()
    try:
        with open(fname, "a", encoding="utf-8") as f:
            f.write(f"{username} : {score}\n")
    except Exception as e:
        print("Error saving result:", e)

def load_scores(fname):
    scores = []
    try:
        with open(fname, "r", encoding="utf-8") as f:
            for line in f:
                if " : " in line:
                    name, scr = line.strip().split(" : ")
                    if scr.isdigit():
                        scores.append((name, int(scr)))
    except FileNotFoundError:
        print(f"File {fname} not found. No results yet.")
    except Exception as e:
        print("Error reading scores:", e)
    return scores

def save_sorted_scores(fname, scores):
    try:
        scores.sort(key=lambda x: x[1], reverse=True)
        with open(fname, "w", encoding="utf-8") as f:
            for name, score in scores:
                f.write(f"{name} : {score}\n")
    except Exception as e:
        print("Error saving leaderboard:", e)

def show_top(scores, top_n=10):
    print("\nTOP PLAYERS:")
    for i, (name, score) in enumerate(scores[:top_n], 1):
        print(f"{i}. {name} - {score}")

def game():
    username = USERNAME or input("Enter your name: ").strip()
    all_questions = get_questions(QUESTIONS_FILE)

    indexes = get_random_indexes(len(all_questions), QUESTIONS_COUNT)
    selected = [all_questions[i] for i in indexes]
    prepared = prepare_questions(selected)

    score = play_quiz(prepared)
    print(f"\nYour result: {score}/{QUESTIONS_COUNT}")

    save_score(TOP, username, score)
    scores = load_scores(TOP)
    save_sorted_scores(TOP, scores)

    if yes == "y":
        show_top(scores)
    elif yes == "n":
        return
    else:
        show = input("Show leaderboard? (y/n): ").strip().lower()
        if show == "y":
            show_top(scores)

if __name__ == "__main__":
    main()