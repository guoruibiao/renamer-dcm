# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'renamerui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(444, 187)
        MainWindow.setFixedSize(444, 187)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 110, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 110, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 70, 291, 21))
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 360, 16))
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(330, 66, 90, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(128, 10, 160, 32))
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 444, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "🍒 DCM 后缀处理"))
        self.pushButton.setText(_translate("MainWindow", "撤销修改"))
        self.pushButton_2.setText(_translate("MainWindow", "确认修改"))
        self.label.setText(_translate("MainWindow", "目标路径"))
        self.pushButton_3.setText(_translate("MainWindow", "选择文件夹"))
        self.label_2.setText(_translate("MainWindow", "嘎嘎蹦蹦的 <font color='green'><strong><blob>dcm</blob></strong></font> 改名神器"))
        # 让输入框获取焦点
        self.lineEdit.setFocus()





class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 中间数据存储
        self.filenames = []
        self.changed_filenames = []
        # 目标后缀名
        self.suffix = ".dcm"
        # 绑定事件
        self._bind_actions()
        self.exclude_extensions = [
            "py"
        ]
        self.exclude_filenames = [
            ".DS_Store",
            "VERSION",
        ]

    def _bind_actions(self):
        # 选取文件路径
        self.pushButton_3.clicked.connect(self._get_directory_path)
        # 绑定修改事件
        self.pushButton_2.clicked.connect(self._change_extension)
        # 绑定撤销事件
        self.pushButton.clicked.connect(self._revoke_extension)
        # lineEdit 改变事件
        self.lineEdit.textChanged.connect(self._line_changed)


    def _get_directory_path(self):
        self.filenames = []
        ftuple = QFileDialog.getOpenFileName(self, "Open File", "./", "Txt (*)")
        if ftuple[0] == "" or "/" not in ftuple[0]:
            self.statusbar.showMessage("文件路径选择失败，请重新选择")
            return
        dirname = "/".join(str(ftuple[0]).split("/")[:-1])
        self.lineEdit.setText(dirname)
        # 读取路径中所有文件
        self._read_all_filenames(dirname)
        print(self.filenames)

    def _line_changed(self, text):
        folder = str(text)
        if os.path.isfile(folder):
            self.label.setText("路径:{}是一个文件，请使用文件夹!".format(folder))
            return
        if not os.path.isdir(folder):
            self.label.setText("路径:{}不是文件夹，请使用文件夹！".format(folder))
            return
        if not os.path.exists(folder):
            self.label.setText("路径:{}不存在，请检查是否正确！".format(folder))
            return
        if str(folder) == "/":
            self.label.setText("路径:{}文件太多，不建议扫描！".format(folder))
            return
        self.label.setText("当前路径检查通过，请确认是否要修改里面的文件为 dcm 文件！")
        # 检查通过即可扫描可处理文件
        print("当前 folder=", folder)
        self._read_all_filenames(folder)
        # 将扫描到的文件内容显示到状态栏
        self.statusbar.showMessage("当前目录扫描到{}个文件！".format(len(self.filenames)))


    def _read_all_filenames(self, path):
        self.filenames = []
        # 判断路径有效性
        if not os.path.isdir(path):
            self.statusbar.showMessage("当前路径：{} 不合法，请重新选择".format(path))
            return
        for root, dir, files in os.walk(path):
            for file in files:
                print(file)
                filename = str(os.path.join(root, file))
                if os.path.isfile(filename) == False:
                    continue
                if file in self.exclude_filenames:
                    continue
                # 判断是否有拓展名，对有拓展名的进行特殊过滤
                if "." in str(file):
                    row = str(file).split(".")
                    if len(row) >= 1 and row[-1] in self.exclude_extensions:
                        continue
                # 加入待更换列表
                self.filenames.append(filename)
        # 将扫描到的文件内容显示到状态栏
        self.statusbar.showMessage("当前目录扫描到{}个文件！".format(len(self.filenames)))

    def _change_extension(self):
        self.changed_filenames = []
        for filename in self.filenames:
            newname = filename + self.suffix
            try:
                os.rename(filename, newname)
            except:
                continue
            self.changed_filenames.append(newname)
        succ = len(self.changed_filenames)
        if succ == 0:
            msg = "暂时没有文件要修改"
        else:
            msg = "成功修改了{}个文件！".format(succ)
        self.statusbar.showMessage(msg)

    def _revoke_extension(self):
        succ = 0
        for filename in self.changed_filenames:
            filename = str(filename)
            if not filename.endswith(self.suffix):
                continue
            newname = os.path.splitext(filename)[0]
            try:
                os.rename(filename, newname)
            except:
                continue
            succ += 1
        # 将改动展示到状态栏
        if succ == 0:
            msg = "暂时没有文件要撤销"
        else:
            msg = "成功撤销了{}个文件！".format(succ)
        self.statusbar.showMessage(msg)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    iconPath = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'raw.jpg')
    app.setWindowIcon(QIcon(iconPath))
    win = Main()
    win.show()
    sys.exit(app.exec_())