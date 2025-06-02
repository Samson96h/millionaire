def get_info(fname):
    with open(fname) as f:
        return f.read()

mstr = get_info('game.txt')
ml = mstr.split('\n')

def get_data(lst):
    md = {}
    ind1 = 0
    ind2 = 4
    while ind2 <= len(lst):
        if lst[ind1] not in md:
            md[lst[ind1]] = []
        md[lst[ind1]]= lst[ind1 + 1:ind2]
        ind1 = ind2
        ind2 += 4
    return md

md = get_data(ml)

def check_winner(board):
    for row in board:
        if row == "xxx":
            return "X"
        elif row == "ooo":
            return "O"

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == "x":
                return "X"
            elif board[0][col] == "o":
                return "O"

    return "D"

def save_results(md, filename):
    with open(filename, "w") as f:
        for game, board in md.items():
            winner = check_winner(board)
            f.write(f"{game.strip("-")} : {winner}\n")

save_results(md, "result.txt")