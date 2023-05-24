import mysql.connector
import collections
import matplotlib.pyplot as plt
import pandas as pd
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

DB = mysql.connector.connect(host='localhost', user="root",
                             password="Cuong461980", database="schedule", port=3306)


class ScheduleApp(QWidget):
    def __init__(self, username=None):
        super(ScheduleApp, self).__init__()
        loadUi("MainApp\\Schedule_Page\\schedule1.ui", self)
        title = "Calendar Manager"
        self.username = username
        self.setWindowTitle(title)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)
        self.deleteButton.clicked.connect(self.deleteTask)
        self.plotButton.clicked.connect(self.plot)

    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        dateSelected = str(dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()
        db = DB
        myCursor = db.cursor()
        myCursor.execute("SELECT task, completed FROM schedule WHERE dates = '" +
                         str(date) + "' " + "AND username = " + "'" + self.username + "'")
        results = myCursor.fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    def saveChanges(self):
        db = DB
        myCursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == Qt.Checked:
                query = "UPDATE `%s` SET `%s` = 'YES'" % (
                    'schedule', 'completed')
            else:
                query = "UPDATE `%s` SET `%s` = 'NO'" % (
                    'schedule', 'completed')
            query += " WHERE `%s` = '" % ('task') + task + "' AND `%s` = '" % ('dates') + str(date) + "' " \
                + "AND `%s` = '" % ('username') + str(self.username) + "' "
            print(query)
            myCursor.execute(query)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        db = DB
        myCursor = db.cursor()

        newTask = str(self.taskLineEdit.text())
        date = str(self.calendarWidget.selectedDate().toPyDate())
        newGroup = str(self.groupComboBox.currentText())

        new_query = "INSERT INTO `%s`(`%s`, `%s`, `%s`, `%s`, `%s`) " % ('schedule', 'dates', 'task', 'completed', 'group', 'username') \
            + "VALUES ('%s', '%s', '%s', '%s', '%s')" % (date,
                                                         newTask, 'NO', newGroup, self.username)
        # print(new_query)
        myCursor.execute(new_query)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()

    def deleteTask(self):
        db = DB
        myCursor = db.cursor()

        date = str(self.calendarWidget.selectedDate().toPyDate())
        task = (self.tasksListWidget.currentItem()).text()
        query = "DELETE FROM `%s` WHERE `%s` = '" % ('schedule', 'task') + task + "' AND `%s` = '" % ('dates') + str(date) + "' " \
                + " AND `%s` = '" % ('username') + str(self.username) + "' "
        print(query)
        myCursor.execute(query)
        db.commit()
        self.taskLineEdit.clear()
        self.updateTaskList(date)

    def plot(self):
        data = self.getData()
        data_task = dict(self.freq(data, 1))
        df = pd.DataFrame({"task": data_task.keys(),
                           "frequency":  data_task.values()})
        print(df)
        name = df["task"]
        times = df["frequency"]
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,
                                       figsize=(25, 16), num='Frequency of task')
        ax1.barh(name, times)
        for s in ['top', 'bottom', 'left', 'right']:
            ax1.spines[s].set_visible(False)

        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')

        ax1.xaxis.set_tick_params(pad=5)
        ax1.yaxis.set_tick_params(pad=10)

        ax1.grid(True, color='grey',
                 linestyle='--', linewidth=0.5,
                 alpha=0.2)

        ax1.invert_yaxis()

        for i in ax1.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5,
                     str(round((i.get_width()), 2)),
                     fontsize=10, fontweight='bold',
                     color='grey')

        ax1.set_title('Schedule in frequency',
                      loc='left', )

        fig.text(0.9, 0.15, 'IoT01-K65', fontsize=12,
                 color='grey', ha='right', va='bottom',
                 alpha=0.7)

        data_group = dict(self.freq(data, 1))
        df = pd.DataFrame({"task": data_group.keys(),
                           "frequency":  data_group.values()})
        print(df)
        name = df["task"]
        times = df["frequency"]
        ax2.barh(name, times)
        for s in ['top', 'bottom', 'left', 'right']:
            ax2.spines[s].set_visible(False)

        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')

        ax2.xaxis.set_tick_params(pad=5)
        ax2.yaxis.set_tick_params(pad=10)

        ax2.grid(True, color='grey',
                 linestyle='--', linewidth=0.5,
                 alpha=0.2)

        ax2.invert_yaxis()

        for i in ax2.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5,
                     str(round((i.get_width()), 2)),
                     fontsize=10, fontweight='bold',
                     color='grey')

        fig.text(0.9, 0.15, 'IoT01-K65', fontsize=12,
                 color='grey', ha='right', va='bottom',
                 alpha=0.7)

        plt.show()

    def freq(self, data, col_index):
        task_freq = {}
        task_list = list(data[col_index])
        task_freq = collections.Counter(task_list)
        return task_freq

    def getData(self):
        db = DB
        myCursor = db.cursor()
        myCursor.execute("Select * from schedule where completed = 'YES'" +
                         "AND `%s` = '" % ('username') + str(self.username) + "' ")
        result = myCursor.fetchall()
        df = pd.DataFrame(result)
        return df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())
