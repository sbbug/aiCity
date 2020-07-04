import time


def get_now_time():
    now_time = time.localtime()
    ntime = "{}:{:0>2d}".format((now_time.tm_hour), (now_time.tm_min % 60))
    return ntime


if __name__ == '__main__':
    # while True:
    #    print('menjinsuo is very handsome!')
    #    time.sleep(600)
    #    nowTime = get_now_time()
    #    print('{} wo hai huo zhe'.format(nowTime))
    for i in range(4):
        if i == 2:
            continue
        print(i)
