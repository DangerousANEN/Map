import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]


class Dialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getImage()
        uic.loadUi('Design.ui', self)
        self.initUI()
        # pixmap = QPixmap(self.img)
        # self.lbl.setPixmap(pixmap)

    # def accept(self):
    #     Dialog.hide(self)

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request, stream=True).raw

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        Image.open(response).save('map.png')

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.getImage()
        self.image.setPixmap(QPixmap('map.png'))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form2 = Dialog()
    form2.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
