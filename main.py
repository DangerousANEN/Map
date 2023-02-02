import sys

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request, stream=True).raw

        if not response:
            raise Exception(f"{response.status_code} ({response.reason}) - {map_request}")

        Image.open(response).save('map.png')

    def initUI(self):
        self.setWindowTitle('Большая задача по Maps API')
        self.getImage()
        self.image.setPixmap(QPixmap('map.png'))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec())
