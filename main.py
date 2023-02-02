import sys
from typing import Tuple, Literal

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.spn = (0.002, 0.002)
        self.initUI()

    def getImage(self, ll: Tuple[float] = (37.530887, 55.703118), spn: Tuple[float] = (0.002, 0.002),
                 l: Literal["map", "sat", "skl"] = "sat"):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, ll))}" + \
                      f"&spn={','.join(map(str, spn))}&l={l}"
        response = requests.get(map_request, stream=True).raw

        if not response:
            raise Exception(f"{response.status_code} ({response.reason}) - {map_request}")

        Image.open(response).save('map.png')

    def initUI(self):
        self.setWindowTitle('Большая задача по Maps API')
        self.getImage()
        self.image.setPixmap(QPixmap('map.png'))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.spn[0] > 0:
            print('PageUp')
            self.spn = tuple(map(lambda m: round(m - 0.001, 3), self.spn))
            self.getImage(spn=self.spn)
            print(self.spn)
            self.image.setPixmap(QPixmap('map.png'))
        elif event.key() == Qt.Key_PageDown:
            print('PageDown')
            self.spn = tuple(map(lambda m: round(m + 0.001, 3), self.spn))
            self.getImage(spn=self.spn)
            print(self.spn)
            self.image.setPixmap(QPixmap('map.png'))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec())
