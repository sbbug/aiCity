

def LoadStyleFromQss(f):
    file = open(f)
    lines = file.readlines()
    file.close()
    res = ''
    for line in lines:
        res += line

    return res