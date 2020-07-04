import time
import os
import signal
# from parameters import START_TIME ,END_TIME

def get_now_time():
    now_time = time.localtime()
    ntime = "{:0>2d}:{:0>2d}".format(now_time.tm_hour, (now_time.tm_min % 60))
    return ntime


def split_time(time):
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    h = 0
    m = 0
    if eval(minute[0])== 0:
        m = eval(minute[1])
    else:
        m = eval(minute)
    if eval(hour[0]) == 0:
        h = eval(hour[1])
    else:
        h = eval(hour)
    return h, m


class control(object):
    def __init__(self, filename):
        '''
        filename : the python file need to be executed
        '''
        self.__file = filename
        pass

    def kill(self, pid):
        try:
            print('pid:', pid)
            os.kill(pid, signal.SIGKILL)
            print('{} : killed'.format(pid))
        except OSError as e:
            print('This process is not exist!')

    def kill_target(self, target):
        cmd_run = "ps aux | grep {}".format(target)
        out = os.popen(cmd_run).read()
        for line in out.splitlines():
            pid = int(line.split()[1])
            self.kill(pid)

    def run(self):
        # print("start")
        os.system('python {} &'.format(self.__file))
        cmd_run = "ps aux | grep {}".format(self.__file)
        out = os.popen(cmd_run).read()
        if out is None:
            print("start failed!")
        else :
            print("started!")


if __name__ == "__main__":
    flag1 = False
    flag2 = True
    istoday = False
    ntime = ""
    # The file and this python file have the same directory.
    # So input file's name directly
    filename = "TestPY.py"  # e.g. test1.py
    # The rule of setting time is %H:%M, moreover 0≤H≤23 and 0≤M≤59
    starttime = "14:00" # e.g. 14:14
    stoptime = "15:21"  # e.g. 14:23
    shour, smin = split_time(starttime)
    sphour, spmin = split_time(stoptime)
    # print("hour is {},min is {}".format(shour, smin))
    # print("hour is {},min is {}".format(sphour, spmin))
    controller = control(filename)
    while True:
        ntime = get_now_time()
        #print(ntime)
        nhour, nmin = split_time(ntime)
        # print("hour is {},min is {}".format(nhour, nmin))
        if nhour > shour or (nhour == shour and nmin >= smin):
            flag1 = True
            start = False
        if flag1 and flag2 and not istoday:
            controller.run()
            flag2 = False
            while True:
                now_time = get_now_time()
                nhour , nmin = split_time(now_time)
                if nhour == sphour and nmin == spmin:
                    break
                else:
                    pass

        if flag1 and not flag2:
            print("stop")
            controller.kill_target(filename)
            flag1 = False
            flag2 = True
            istoday = True
           # break
        while istoday:
            nowTime = get_now_time()
            nhour, nmin = split_time(nowTime)
            if nhour == 0 and nmin == 0:
                istoday = False

