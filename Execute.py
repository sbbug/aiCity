import time
import os
import signal
from Parameters import START_TIME, END_TIME
from Tool.logger.make_logger import make_logger
from DB.SQL_save import createLogDir

save_dir = createLogDir()
logger = make_logger('contorl', save_dir, 'execute_log')

def get_now_time():
    now_time = time.localtime()
    ntime = "{:0>2d}:{:0>2d}".format(now_time.tm_hour, (now_time.tm_min % 60))
    return ntime


def get_this_date():
    day = time.localtime()
    return str(day.tm_year) + str(day.tm_mon) + str(day.tm_mday)


def split_time(time):
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    h = 0
    m = 0
    if eval(minute[0]) == 0:
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

        # log = get_this_date() + ' ' + get_now_time() + ' {} stoped\n'.format(self.__file)
        log = '{} stoped\n'.format(self.__file)
        logger.info(log)

    def run(self):
        global logger
        flag = False
        print("start")
        while True:
            os.system('python {} &'.format(self.__file))
            cmd_run = "ps -aux | grep {}".format(self.__file)
            out = os.popen(cmd_run).read()
            if out is not None:
                flag = True
                break

        if flag:
            print("~started!")
            # log = get_this_date() + ' ' + get_now_time() + ' {} started\n'.format(self.__file)
            log = '{} started\n'.format(self.__file)
            logger.info(log)
        else:
            pass


if __name__ == "__main__":
    from DB.SQL_save import update_feedback
    flag1 = False
    flag2 = True
    istoday = False
    con_f = True
    ntime = ""
    # The file and this python file have the same directory.
    # So input file's name directly
    filename = "NewMainWindow.py"  # e.g. test1.py
    # filename2 = "DB/SQL_save.py"

    # The rule of setting time is %H:%M, moreover 0≤H≤23 and 0≤M≤59
    starttime = START_TIME  # e.g. 14:14
    stoptime = END_TIME  # e.g. 14:23
    startupdate = "20:00"
    shour, smin = split_time(starttime)
    sphour, spmin = split_time(stoptime)
    suhour, sumin = split_time(startupdate)
    # print("hour is {},min is {}".format(shour, smin))
    # print("hour is {},min is {}".format(sphour, spmin))
    controller = control(filename)
    # controller2 = control(filename2)
    while True:
        ntime = get_now_time()
        # print(ntime)
        nhour, nmin = split_time(ntime)
        # print("hour is {},min is {}".format(nhour, nmin))
        if sphour > nhour > shour or (nhour == shour and nmin >= smin):
            flag1 = True
            start = False
        if flag1 and flag2 and not istoday:
            controller.run()
            flag2 = False
            while True:
                now_time = get_now_time()
                nhour, nmin = split_time(now_time)
                if nhour == sphour and nmin == spmin:
                    break
                else:
                    pass
        if flag1 and not flag2:
            print("stop")
            controller.kill_target(filename)
            flag1 = False
            flag2 = True
            # break

        now_time = get_now_time()
        nhour, nmin = split_time(now_time)
        if nhour == suhour and nmin >= sumin:
            update_feedback()
            log = 'DB\SQL_save.py started\n'
            logger.info(log)
            istoday = True
        else:
            pass

        while istoday:
            nowTime = get_now_time()
            nhour, nmin = split_time(nowTime)
            if nhour == 0 and nmin == 1:
                istoday = False
                del logger
                logger = make_logger('contorl', createLogDir(), 'execute_log')

                break
            else:
                pass
