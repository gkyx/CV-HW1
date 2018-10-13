import cv2
import sys
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):


	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("PyQT5")
		self.setWindowState(QtCore.Qt.WindowMaximized)
		self.show()

		self.imgnum = 1

		inputAction = QtWidgets.QAction("Open Input", self)
		inputAction.triggered.connect(lambda: self.open_image(1))

		targetAction = QtWidgets.QAction("Open Target", self)
		targetAction.triggered.connect(lambda: self.open_image(2))

		exitAction = QtWidgets.QAction("Exit", self)
		exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

		equalizeHistAction = QtWidgets.QAction("Equalize Histogram", self)
		equalizeHistAction.triggered.connect(self.equalize_histogram)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(inputAction)
		fileMenu.addAction(targetAction)
		fileMenu.addAction(exitAction)

		self.toolBar = self.addToolBar("ToolBar")
		self.toolBar.addAction(equalizeHistAction)


	def open_image(self, imgSelect):
		print(imgSelect)
		# extract the histograms

	def equalize_histogram(self):
		print(self.imgnum)
		self.open_image(3) # show the created image

	def calc_histogram(self, I):
		R, C, B = I.shape

		hist = np.zeros([256, 1, B], dtype='int64')

		for g in range(256):
			hist[g, 0, ...] = np.sum(np.sum(I == g, 0), 0)

		return hist


def main():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

main()



#image = cv2.imread("color1.png")
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("1", image)
#cv2.imshow("2", gray_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()