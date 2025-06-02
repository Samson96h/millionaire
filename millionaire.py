from random import randint, shuffle

QUESTIONS_COUNT = 5

def player_or_admin ():
    answ = input("Want to start a game or add new questions? play or edit : ")
    if answ == "play":
        game()
    if answ == "edit":
        login = input("Enter password : ")
        if login == "admin":
            edit()
        else:
            print('wrong password')

def edit():
    new_quest = input("Please type the new question: ").strip()

    if not new_quest.endswith("?"):
        new_quest += "?"

    answer_input = input("Enter 4 answers (first one is correct), separated by commas: ").strip()
    answers = [a.strip() for a in answer_input.split(",")]

    if len(answers) != 4:
        print("You must enter exactly 4 answers (1 correct + 3 incorrect).")
        return
    
    question_line = new_quest + ",".join(answers)

    f = open("questions.txt", "a")
    f.write(question_line + "\n")
    f.close()
    
    print("Your question has been added successfully.")



def get_questions(fname):
    with open(fname) as f:
        return [line.strip() for line in f.readlines() if "?" in line]

def get_random_indexes(qcount, count):
    indexes = []
    while len(indexes) < count:
        ind = randint(0, qcount - 1)
        if ind not in indexes:
            indexes.append(ind)
    return indexes

def prepare_questions(questions):
    final = []
    for q in questions:
        if "?" in q:
            q_text, ans_text = q.split("?", 1)
            q_text += "?"
            answers = [a.strip() for a in ans_text.split(",")]
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

        choice = input("Your answer (1-4): ")

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 4:
                answer = q["variants"][num - 1]
            else:
                print("Invalid number! Must be between 1 and 4.")
                answer = ""
        else:
            print("Invalid input! Please enter a number.")
            answer = ""

        if answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            if answer != "":
                print(f"Wrong! Correct answer was: {q['correct']}")
    
    return score


def save_score(fname, username, score):
    with open(fname, "a") as f:
        f.write(f"{username} : {score}\n")

def load_scores(fname):
    scores = []
    with open(fname, "r") as f:
        for line in f:
            if " : " in line:
                name, scr = line.strip().split(" : ")
                if scr.isdigit():
                    scores.append((name, int(scr)))
    return scores

def save_sorted_scores(fname, scores):
    scores.sort(key=lambda x: x[1], reverse=True)
    with open(fname, "w") as f:
        for name, score in scores:
            f.write(f"{name} : {score}\n")

def show_top(scores, top_n=10):
    print("\nTOP PLAYERS:")
    for i, (name, score) in enumerate(scores[:top_n], 1):
        print(f"{i}. {name} - {score}")

def game():
    username = input("Enter your username: ")
    all_questions = get_questions("questions.txt")
    indexes = get_random_indexes(len(all_questions), QUESTIONS_COUNT)
    selected = [all_questions[i] for i in indexes]
    prepared = prepare_questions(selected)
    score = play_quiz(prepared)
    print(f"\nYour final score: {score}/{QUESTIONS_COUNT}")
    
    save_score("top.txt", username, score)
    scores = load_scores("top.txt")
    save_sorted_scores("top.txt", scores)

    show = input("Do you want to see the top players? (y/n): ")
    if show.lower() == "y":
        show_top(scores)

player_or_admin()