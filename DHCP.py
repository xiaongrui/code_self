import os,re
import ctypes
import sys


class IpManage:

    def __init__(self):

        self.ip_list = self.get_ip()


    def set_ip(self,name,ip="192.168.1.123",mask="255.255.255.0",gateway="192.168.1.1"):
        command = f'''netsh interface ip set address name="{name}" static {ip} {mask} {gateway}'''
        runas = "runas /savecred /user:Administrator "
        print(command)
        process = os.popen(command)
        print(process.read())

    def set_ip_dhcp(self,name):
        command = f'''netsh interface ip set address name="{name}" source=dhcp'''
        runas = "runas /savecred /user:Administrator "
        print(command)
        process = os.popen(command)
        print(process.read())

    def get_ip(self):

        result = os.popen('ipconfig')
        res = result.read()
        resultlist = re.findall('''(?<=以太网适配器 ).*?(?=:)|(?<=无线局域网适配器 ).*?(?=:)''', res)
        print(resultlist)
        return resultlist

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == '__main__':

    im = IpManage()
    if im.is_admin():
        # card_id_in = input("选择要设置的网卡序号(从0开始)：")
        card_id_in = 5
        source_in = input("0-静态IP, 1-DHCP:")
        if card_id_in == "":
            card_id = 5
        else:
            card_id = int(card_id_in)
        if source_in == "":
            source = 0
        else:
            source = int(source_in)

        if source == 0:
            im.set_ip(im.ip_list[card_id])
            # im.set_DNS(im.ip_list[card_id])
            print(im.ip_list[card_id]," 静态IP设置完成！")
        else:
            im.set_ip_dhcp(im.ip_list[card_id])
            print(im.ip_list[card_id]," 动态IP设置完成！")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)