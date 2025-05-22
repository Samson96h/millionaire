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
    player_name = input("Please enter your name : ")
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

    with open("top.txt", "a") as f:
        f.write(player_name + ' : ' + str(score) + "\n")

    with open("top.txt", "r") as f:
        results = f.readlines()
    scores = []
    for line in results:
        line = line.strip()
        if " : " in line:
            info = line.split(" : ")
            if len(info) == 2 and info[1].isdigit():
                name = info[0]
                score = int(info[1])
                scores.append((name, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    with open("top.txt", "w") as f:
        for name, score in scores:
            f.write(f"{name} : {score}\n")

    def top_players():
        print("\n TOP PLAYERS ")
        for i, (name, score) in enumerate(scores[:10], 1):
            print(f"{i}. {name} - {score}")

    answer = input("Do you want to see the best players? y / n: ")
    if answer.lower() == "y":
        top_players()

run_quiz()