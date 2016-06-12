'''
Created on 05/06/2016

@author: botpi
'''

def save_case_gap(district_id, data):
    with open("txt/case_gap_"+ str(district_id) + ".txt", "w") as f:
        c = 0
        for d in data:
            if c == len(data)-1:
                f.write(str(d))
            else:
                f.write(str(d)+",")
                c += 1
    f.close()

def read_case_gap(district_id):
    f = open("txt/case_gap_"+ str(district_id) + ".txt", "rb")
    data = f.read().split(",")
    f.close()
    if data == ['']:
        return []
    else:
        return [int(x) for x in data]

def save_case(district_id, data):
    with open("txt/case_"+ str(district_id) + ".txt", "w") as f:
        c = 0
        for d in data:
            if c == len(data)-1:
                f.write(str(d))
            else:
                f.write(str(d)+",")
                c += 1
    f.close()

def read_case(district_id):
    f = open("txt/case_"+ str(district_id) + ".txt", "rb")
    data = f.read().split(",")
    f.close()
    if data == ['']:
        return []
    else:
        return [int(x) for x in data]
    # data = f.read()
    # case = []
    # for d in data.split(","):
    #     case.append(int(d))
    # return  case

def save_score(district_id, score):
    f = open("txt/score_"+ str(district_id) + ".txt", "w")
    score += 0.000000000001
    f.write(str(score))
    f.close()

def read_score(district_id):
    f = open("txt/score_"+ str(district_id) + ".txt", "rb")
    data = f.read()
    f.close()
    return float(data)

def save_l(district_id, score):
    f = open("txt/l_"+ str(district_id) + ".txt", "w")
    f.write(str(score))
    f.close()

def read_l(district_id):
    f = open("txt/l_"+ str(district_id) + ".txt", "rb")
    data = f.read()
    f.close()
    return int(data)

def save_l_2(district_id, score):
    f = open("txt/l_2_"+ str(district_id) + ".txt", "w")
    f.write(str(score))
    f.close()

def read_l_2(district_id):
    f = open("txt/l_2_"+ str(district_id) + ".txt", "rb")
    data = f.read()
    f.close()
    return int(data)

def save_case2(data):
    with open("case2.txt", "w") as f:
        c = 0
        for d in data:
            if c == len(data)-1:
                f.write(str(d))
            else:
                f.write(str(d)+",")
                c += 1
    f.close()

def read_case2():
    f = open("case2.txt", "rb")
    data = f.read()
    case = []
    for d in data.split(","):
        case.append(int(d))
    f.close()
    return  case

def save_score2(score):
    f = open("score2.txt", "w")
    score += 0.000000000001
    f.write(str(score))
    f.close()

def read_score2():
    f = open("score2.txt", "rb")
    data = f.read()
    f.close()
    return float(data)
