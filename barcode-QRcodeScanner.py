from __future__ import print_function

from threading import Thread

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import sys

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from time import sleep

import csv

from gui import Ui_Fcode

class MainWindow(QtWidgets.QMainWindow):
    listData = []

    def __init__(self):
        super().__init__()
        self.uic = Ui_Fcode()
        self.uic.setupUi(self)

        # set the title
        self.setWindowTitle("Phạm Trung Kỳ - Nguyễn Hương Mai")

        # Worker 1
        self.workerThread = WorkerThread()
        self.workerThread.start()
        self.workerThread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.workerThread.Data.connect(self.DataReady)
        self.workerThread.List.connect(self.ListReady)
        self.uic.CancelBTN.clicked.connect(self.CancelFeed)

    def DataReady(self, data):
        self.uic.QrCodeData.setText(data)

    def ListReady(self, list):
        self.uic.listWidget.clear()
        self.uic.listWidget.addItems(list)
        self.listData = list

    def ImageUpdateSlot(self, Image):
        self.uic.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def threaded_function(self):
        with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.listData)
            sleep(0.01)

    def CancelFeed(self, list):
        # self.workerThread.stop()
        # print("Hello")
        thread = Thread(target=self.threaded_function)
        thread.start()
        thread.join()
        print("Done")


class WorkerThread(QtCore.QThread):
    ImageUpdate = pyqtSignal(QImage)
    Data = pyqtSignal(object)
    List = pyqtSignal(list)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        list = []
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # =================================================
                decodedObjects = pyzbar.decode(frame)

                # Print results
                for obj in decodedObjects:

                    #
                    item = str(obj.data.decode("utf-8"))
                    if item in list:
                        pass
                    else:
                        list.append(str(obj.data.decode("utf-8")))
                        self.List.emit(list)
                        sleep(0.01)

                    # Display barcode and QR code location
                    if obj.type == "QRCODE":
                        points = obj.polygon

                        # If the points do not form a quad, find convex hull
                        if len(points) > 4:
                            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                            hull = list(map(tuple, np.squeeze(hull)))
                        else:
                            hull = points;

                        # Number of points in the convex hull
                        n = len(hull)

                        # Draw the convext hull
                        for j in range(0, n):
                            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
                        # =================================================
                        self.Data.emit(str(obj.data.decode("utf-8")))
                        sleep(0.01)

                # Export image
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                sleep(0.01)

    def stop(self):
        self.ThreadActive = False
        self.quit()


# Main
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
