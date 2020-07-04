from ftplib import FTP
import time
import os


class FtpServer:

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.server_root = "/data/ftp/"
        self.locol_root = "G:/companyProject/now/cityManager/data/virtualCameraData/"
        self.old_img_path = ""
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

    def loadload_img(self):
        '''
        :return:
        '''
        list_file_name = self.ftp_handler.nlst()
        sorted(list_file_name)
        dir = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        now_dir_path = os.path.join(self.locol_root, dir)
        if not os.path.exists(now_dir_path):
            os.mkdir(now_dir_path)
        self.old_img_path = os.path.join(now_dir_path, list_file_name[-1])
        img_file = open(self.old_img_path, "wb")
        self.ftp_handler.retrbinary('RETR ' + list_file_name[-1], img_file.write, 1024)
        img_file.close()

        return self.old_img_path

    def quit(self):
        '''
        :return:
        '''
        self.ftp_handler.quit()


if __name__ == "__main__":
    ftp_server = FtpServer("121.43.182.244", 'ftpuser', 'Lawatlas2018')
    ftp_server.loadload_img()

