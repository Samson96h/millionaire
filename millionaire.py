import random

def get_quest(fname):
    f = open(fname)
    lines = f.readlines()
    f.close()
    return lines

quest_list = get_quest("questions.txt")

def questions_craft(list):
    md_quest = []
    for i in list:
        i = i.strip()
        ind = i.index("?")
        question = i[:ind + 1]
        answers = [a.strip() for a in i[ind + 1:].split(",")]
        md_quest.append({
            "question": question,
            "answers": answers,
            "correct": answers[0]
        })
    return random.sample(md_quest, 10)

def run_quiz():
    quests = questions_craft(get_quest("questions.txt"))
    score = 0
    for q in quests:
        print("\n" + q["question"])
        random.shuffle(q["answers"])
        for i, answer in enumerate(q["answers"], 1):
            print(f"{i}. {answer}")

        user = int(input("Your answer please (1 - 4): "))
        user = q["answers"][user - 1]
        if user == q["correct"]:
            print("YESSS !")
            score += 1
        else:
            print(f"NOOO ! {q['correct']}")

    print(f"Your score : {score} / 10")

run_quiz()