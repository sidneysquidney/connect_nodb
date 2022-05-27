from grid import PDICT

def score_by_piece(lsts):
    # score function that takes how many single pieces are active (able to make a winning four in the future)
    score = 0
    for lst in lsts:
        sett, count, length, zeros = set(), 0, 0, 0
        for n in lst:
            sett.add(PDICT[n].score)
            if sett.intersection({1,-1}) == {1, -1}:
                if length >= 4:
                    score += count * sum(sett.difference({PDICT[n].score}))
                sett = {PDICT[n].score}
                count = 1 
                length = 1 + zeros
                zeros = 0
                continue
            if n != 0:
                zeros = 0
                count += 1
            else: 
                zeros += 1
            length += 1
        if length >= 4:
            score += count * sum(sett)
    return score    

def score_by_line(lsts):
    # score function that says how many lines are active and can be filled to win
    score = 0
    for lst in lsts:
        sub_list = [lst[i: i + 4] for i in range(len(lst) - 3)]
        lst_score = set()
        for sub in sub_list:
            four_score = set()
            for n in sub:
                four_score.add(PDICT[n].score)
            lst_score.add(sum(four_score))
        score += sum(lst_score)
    return score