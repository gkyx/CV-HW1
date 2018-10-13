import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):


	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("PyQT5")
		self.setWindowState(QtCore.Qt.WindowMaximized)
		self.show()

		self.imgnum = 1
		self.hist1 = None
		self.hist2 = None

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

		if self.hist1 is not None and self.hist2 is not None:
			K = np.zeros([R, C, B], dtype=np.uint8)

			L = self.lookup_creator(self.hist1, self.hist2)
			for i in range(R):
				for j in range(C):
					K[i][j][0] = L[0, Img1[i][j][0], 0]
					K[i][j][1] = L[1, Img1[i][j][1], 0]
					K[i][j][2] = L[2, Img1[i][j][2], 0]

			return K

		else:
			msg = QtWidgets.QMessageBox.warning(self, "Warning", "Both Input and Target images must be open to continue to this job!", QtWidgets.QMessageBox.Ok)
			return None

	def lookup_creator(self, pdf1, pdf2):
		cdf1 = np.zeros([256, 1, 3], dtype='int64')
		cdf2 = np.zeros([256, 1, 3], dtype='int64')
		
		LUT = np.zeros([3, 256, 1], dtype=np.uint8)

		# create cdf of the images by going through the pdf and summing the pdf values in a cuulative fashion

		for i in range(256):
			if i == 0:
				cdf1[0, 0, 0] = int(pdf1[0, 0, 0])
				cdf1[0, 0, 1] = int(pdf1[0, 0, 1])
				cdf1[0, 0, 2] = int(pdf1[0, 0, 2])

				cdf2[0, 0, 0] = int(pdf2[0, 0, 0])
				cdf2[0, 0, 1] = int(pdf2[0, 0, 1])
				cdf2[0, 0, 2] = int(pdf2[0, 0, 2])
			else:
				cdf1[i, 0, 0] = int(cdf1[i - 1, 0, 0] + pdf1[i, 0, 0])
				cdf1[i, 0, 1] = int(cdf1[i - 1, 0, 1] + pdf1[i, 0, 1])
				cdf1[i, 0, 2] = int(cdf1[i - 1, 0, 2] + pdf1[i, 0, 2])

				cdf2[i, 0, 0] = int(cdf2[i - 1, 0, 0] + pdf2[i, 0, 0])
				cdf2[i, 0, 1] = int(cdf2[i - 1, 0, 1] + pdf2[i, 0, 1])
				cdf2[i, 0, 2] = int(cdf2[i - 1, 0, 2] + pdf2[i, 0, 2])

		j = 0

		# red look up table
		for i in range(256):
			while cdf2[j, 0, 0] < cdf1[i, 0, 0] and j < 255:
				print(cdf1[i, 0, 0], cdf2[j, 0, 0])
				j += 1
			
			LUT[0, i, 0] = j

		j = 0
		# green look up table
		for i in range(256):
			while cdf2[j, 0, 1] < cdf1[i, 0, 1] and j < 255:
				j += 1
			
			LUT[1, i, 0] = j

		j = 0
		# blue look up table
		for i in range(256):
			while cdf2[j, 0, 2] < cdf1[i, 0, 2] and j < 255:
				j += 1
			
			LUT[2, i, 0] = j

		return LUT

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