import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):


	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("Histogram Equalization")
		self.setWindowState(QtCore.Qt.WindowMaximized)

		self.imgnum = 1
		self.hist1 = None
		self.hist2 = None
		self.hist3 = None
		self.Img1 = None
		self.Img2 = None
		self.isInputOpen = False
		self.isTargetOpen = False

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

		self.centralwidget = QtWidgets.QWidget(self)
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setContentsMargins(100, 10, 100, 10)
		self.horizontalLayout.setSpacing(100)
		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.VerticalLayout1 = QtWidgets.QVBoxLayout(self.widget)
		self.VerticalLayout1.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout1.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget)
		self.widget_2 = QtWidgets.QWidget(self.centralwidget)
		self.widget_2.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.VerticalLayout2 = QtWidgets.QVBoxLayout(self.widget_2)
		self.VerticalLayout2.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout2.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget_2)
		self.widget_3 = QtWidgets.QWidget(self.centralwidget)
		self.widget_3.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.VerticalLayout3 = QtWidgets.QVBoxLayout(self.widget_3)
		self.VerticalLayout3.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout3.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget_3)
		self.setCentralWidget(self.centralwidget)
		
		self.show()


	def open_image(self, imgSelect):
		if imgSelect == 1 and not self.isInputOpen:
			self.Img1 = cv2.imread("color2.png")
			self.hist1 = self.calc_histogram(self.Img1)
			
			# Image

			pix = QtGui.QPixmap('color2.png')
			label = QtWidgets.QLabel(self.widget)
			label.setPixmap(pix)
			label.setAlignment(QtCore.Qt.AlignCenter)
			label.setStyleSheet("border:0px")
			self.VerticalLayout1.addWidget(label)

			# histograms

			plt.gcf().clear()
			plt.subplot(3,1,1)
			plt.bar(range(256), self.hist1[:,0,2], align='center', alpha=0.5, color='#FF0000')
			plt.subplot(3,1,2)
			plt.bar(range(256), self.hist1[:,0,1], align='center', alpha=0.5, color='#00FF00')
			plt.subplot(3,1,3)
			plt.bar(range(256), self.hist1[:,0,0], align='center', alpha=0.5, color='#0000FF')
			
			plt.savefig("./inputHistogram.png", dpi=80)

			pix2 = QtGui.QPixmap('inputHistogram.png')
			label2 = QtWidgets.QLabel(self.widget)
			label2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
			label2.setPixmap(pix2)
			label2.setAlignment(QtCore.Qt.AlignCenter)
			label2.setStyleSheet("border:0px")
			self.VerticalLayout1.addWidget(label2)

			self.isInputOpen = True

		elif imgSelect == 2 and not self.isTargetOpen:
			self.Img2 = cv2.imread("color1.png")
			
			self.R, self.C, self.B = self.Img2.shape

			self.hist2 = self.calc_histogram(self.Img2)
			
			# Image

			pix = QtGui.QPixmap('color1.png')
			label = QtWidgets.QLabel(self.widget_2)
			label.setPixmap(pix)
			label.setAlignment(QtCore.Qt.AlignCenter)
			label.setStyleSheet("border:0px")
			self.VerticalLayout2.addWidget(label)

			# histograms

			plt.gcf().clear()
			plt.subplot(3,1,1)
			plt.bar(range(256), self.hist2[:,0,2], align='center', alpha=0.5, color='#FF0000')
			plt.subplot(3,1,2)
			plt.bar(range(256), self.hist2[:,0,1], align='center', alpha=0.5, color='#00FF00')
			plt.subplot(3,1,3)
			plt.bar(range(256), self.hist2[:,0,0], align='center', alpha=0.5, color='#0000FF')
			
			plt.savefig("./targetHistogram.png", dpi=80)

			pix2 = QtGui.QPixmap('targetHistogram.png')
			label2 = QtWidgets.QLabel(self.widget_2)
			label2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
			label2.setPixmap(pix2)
			label2.setAlignment(QtCore.Qt.AlignCenter)
			label2.setStyleSheet("border:0px")
			self.VerticalLayout2.addWidget(label2)

			self.isTargetOpen = True


	def equalize_histogram(self):
		if self.hist1 is not None and self.hist2 is not None:
			K = np.zeros([self.R, self.C, self.B], dtype=np.uint8)

			L = self.lookup_creator(self.hist1, self.hist2)
			for i in range(self.R):
				for j in range(self.C):
					K[i][j][0] = L[0, self.Img1[i][j][0], 0]
					K[i][j][1] = L[1, self.Img1[i][j][1], 0]
					K[i][j][2] = L[2, self.Img1[i][j][2], 0]

			cv2.imwrite("./equalized.png", K)

			self.hist3 = self.calc_histogram(K)
			
			# Image

			pix = QtGui.QPixmap('equalized.png')
			label = QtWidgets.QLabel(self.widget_3)
			label.setPixmap(pix)
			label.setAlignment(QtCore.Qt.AlignCenter)
			label.setStyleSheet("border:0px")
			self.VerticalLayout3.addWidget(label)

			# histograms

			plt.gcf().clear()
			plt.subplot(3,1,1)
			plt.bar(range(256), self.hist3[:,0,2], align='center', alpha=0.5, color='#FF0000')
			plt.subplot(3,1,2)
			plt.bar(range(256), self.hist3[:,0,1], align='center', alpha=0.5, color='#00FF00')
			plt.subplot(3,1,3)
			plt.bar(range(256), self.hist3[:,0,0], align='center', alpha=0.5, color='#0000FF')
			
			plt.savefig("./equalizedHistogram.png", dpi=80)

			pix2 = QtGui.QPixmap('equalizedHistogram.png')
			label2 = QtWidgets.QLabel(self.widget_3)
			label2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
			label2.setPixmap(pix2)
			label2.setAlignment(QtCore.Qt.AlignCenter)
			label2.setStyleSheet("border:0px")
			self.VerticalLayout3.addWidget(label2)

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

		# blue look up table
		for i in range(256):
			while cdf2[j, 0, 0] < cdf1[i, 0, 0] and j < 255:
				j += 1
			
			LUT[0, i, 0] = j

		j = 0
		# green look up table
		for i in range(256):
			while cdf2[j, 0, 1] < cdf1[i, 0, 1] and j < 255:
				j += 1
			
			LUT[1, i, 0] = j

		j = 0
		# red look up table
		for i in range(256):
			while cdf2[j, 0, 2] < cdf1[i, 0, 2] and j < 255:
				j += 1
			
			LUT[2, i, 0] = j

		return LUT
  
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