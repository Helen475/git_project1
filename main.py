import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM coffe """).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

        self.pushButton.clicked.connect(self.runform2)
        self.pushButton_2.clicked.connect(self.bdupdate)

    def runform2(self):
        self.form2 = MyForm2()
        self.form2.show()

    def bdupdate(self):
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM coffe """).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


class MyForm2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.db")

        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.update_result)
        self.pushButton.clicked.connect(self.addcoffee)
        self.modified = {}
        self.titles = None

    def addcoffee(self):
        cur = self.con.cursor()
        s = f"INSERT INTO coffe (name, roasting, type, taste, price, volume) VALUES ("
        s += f"'{self.tableWidget1.item(0, 1).text()}', "
        s += f"'{self.tableWidget1.item(0, 2).text()}', "
        s += f"'{self.tableWidget1.item(0, 3).text()}', "
        s += f"'{self.tableWidget1.item(0, 4).text()}', "
        s += f"'{int(self.tableWidget1.item(0, 5).text())}', "
        s += f"'{int(self.tableWidget1.item(0, 6).text())}')"
        print(s)
        cur.execute(s).fetchall()
        self.con.commit()

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()
        print(self.modified)

    def save_results(self):
            if self.modified:
                cur = self.con.cursor()
                que = "UPDATE coffe SET\n"
                que += ", ".join([f"{key}='{self.modified.get(key)}'"
                                  for key in self.modified.keys()])
                que += "WHERE id = ?"
                cur.execute(que, (self.spinBox.text(),))
                self.con.commit()
                self.modified.clear()

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffe WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())