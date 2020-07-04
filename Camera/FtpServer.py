from ftplib import FTP
import time
import os
import cv2


class FtpServer:

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.server_root = "/data/ftp/"
        self.local_root = "/home/user/code/cityManager/Resources/FtpServer/"
        self.old_img_path = ""  # default
        self.thread_running = False
        self.init_con()

    def init_con(self):
        '''
        :return:
        '''
        try:
            self.ftp_handler = FTP(self.ip)
            self.ftp_handler.login(self.username, self.password)
            self.ftp_handler.set_pasv(False)
            self.ftp_handler.cwd(self.server_root)
        except:
            print("fpt conection have a error")

    def load_img(self):
        '''
        :return:
        '''
        try:

            list_file_name = self.ftp_handler.nlst()

            list_file_name = [name for name in list_file_name if str(name).startswith("10.216.99.173") is True]

            sorted(list_file_name, key=lambda x: x.split("_")[2])
            # sorted(list_file_name, key=lambda x: x.split("_")[2] if str(x).startswith("10.216.99.173") is True else continue)
            dir = time.strftime('%Y-%m-%d', time.localtime(time.time()))

            now_dir_path = os.path.join(self.local_root, dir)

            if not os.path.exists(now_dir_path):
                os.mkdir(now_dir_path)
            print(list_file_name)
            self.old_img_path = os.path.join(now_dir_path, list_file_name[-1])
            img_file = open(self.old_img_path, "wb")
            self.ftp_handler.retrbinary('RETR ' + list_file_name[-1], img_file.write, 1024)

            img_file.close()
        except:
            print(os.path.getsize(self.old_img_path))
            print(self.old_img_path)
            print("ftp get image is failed")

        return self.old_img_path

    def read(self):

        img_path = self.load_img()

        if img_path is "":
            return None

        if os.path.getsize(self.old_img_path) is 0:
            return None

        return cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

    def quit(self):
        '''
        :return:
        '''
        self.thread_running = False
        self.ftp_handler.quit()


if __name__ == "__main__":
    ftp_server = FtpServer("121.43.182.244", 'ftpuser', 'Lawatlas2018')

    print(ftp_server.read())
