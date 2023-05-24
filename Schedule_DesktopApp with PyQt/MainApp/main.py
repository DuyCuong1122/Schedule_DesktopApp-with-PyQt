import mysql.connector
import sys
from datetime import date
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox, QMainWindow, QDialog, QStackedWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from Schedule_Page.schedule import ScheduleApp

DB = mysql.connector.connect(host='localhost', user="root",
                             password="Cuong461980", database="schedule", port=3306)


class LoginApp(QDialog):
    def __init__(self, window):
        super(LoginApp, self).__init__()
        title = "Login"
        # set the title
        self.setWindowTitle(title)
        loadUi("MainApp\\Login_Register_Page\\login.ui", self)
        self.loginButton.clicked.connect(self.login)
        self.signupButton.clicked.connect(self.signUp)
        self.window = window

    # hàm login sử dụng module mysql-connector kết nối database trên web

    def login(self):
        un = self.userName.text()
        pw = self.password.text()
        # kết nối mysql
        db = DB
        myCursor = db.cursor()
        myCursor.execute("Select * from login where username = '" +
                         un + "' and password = '" + pw + "' ")
        result = myCursor.fetchone()
        if result:
            QMessageBox.about(self, "Login output",
                              "Successfully logged in!!!")
            # w.setCurrentIndex(0)
            self.scheduleGet()
        else:
            QMessageBox.about(self, "Login output", "Failed to login")

    def signUp(self, schedule):
        w.setCurrentIndex(1)

    def scheduleGet(self):
        self.window.username = self.userName.text()
        self.window.updateTaskList(str(date.today()))
        print(self.window.username)
        self.window.resize(1600, 800)
        self.window.show()


class RegApp(QDialog):
    def __init__(self):
        super(RegApp, self).__init__()
        loadUi("MainApp\\Login_Register_Page\\register.ui", self)
        title = "Register"

        # set the title
        self.setWindowTitle(title)
        self.signUpBt.clicked.connect(self.register)
        self.loginNow.clicked.connect(self.show_login)

    def register(self):
        em = self.email.text()
        un = self.Username.text()
        pw = self.password.text()
        db = DB
        myCursor = db.cursor()
        myCursor.execute("Select * from login where username = '" + un + "' ")
        result = myCursor.fetchone()
        if result:
            QMessageBox.information(
                self, "Login form", "The username is already registered, please try other username!!!")
        else:
            new_query = "INSERT INTO `%s`(`%s`, `%s`, `%s`) " % ('login', 'email', 'username', 'password') \
                + "VALUES ('%s', '%s', '%s')" % (em, un, pw)
            myCursor.execute(new_query)
            db.commit()
            QMessageBox.information(
                self, "Login form", "The username registered successfully, You can login now!")

    def show_login(self):
        w.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QStackedWidget()
    w.setWindowTitle("App manager")
    window = ScheduleApp("")
    loginform = LoginApp(window)
    regisForm = RegApp()
    # Thêm form login và form register vào QStackedWidget
    w.addWidget(loginform)
    w.addWidget(regisForm)
    w.setCurrentIndex(0)
    w.setFixedWidth(1600)
    w.setFixedHeight(1200)
    w.show()

    app.exec()
