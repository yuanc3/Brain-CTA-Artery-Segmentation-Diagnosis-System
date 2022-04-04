import MyWindow_server as MyWindow
from sys import argv
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(argv)  # 创建一个应用对象 ,sys.argv 是提供对脚本控制功能的参数
    # 实例化对象
    ex = MyWindow.MyWindow()
    # 结束应用的主循环，主循环是从窗口系统中接受时间并快速的法网应用窗口，调用exit()方法或者主窗口关闭时，主循环结束
    ex.show()
    # sys.exec_()方法是确保关闭干净
    #sys.exit(app.exec_())
    app.exec_()