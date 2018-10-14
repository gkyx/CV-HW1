import cv2
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):


	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("Histogram Equalization")
		self.setWindowState(QtCore.Qt.WindowMaximized)

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

		self.centralwidget = QtWidgets.QWidget(self)
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setContentsMargins(100, -1, 100, -1)
		self.horizontalLayout.setSpacing(100)
		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.horizontalLayout.addWidget(self.widget)
		self.widget_2 = QtWidgets.QWidget(self.centralwidget)
		self.widget_2.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.horizontalLayout.addWidget(self.widget_2)
		self.widget_3 = QtWidgets.QWidget(self.centralwidget)
		self.widget_3.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		self.horizontalLayout.addWidget(self.widget_3)
		self.setCentralWidget(self.centralwidget)
		
		self.show()


	def open_image(self, imgSelect):
		if imgSelect == 1:
			ImgArray = cv2.imread("color2.png")
			self.hist1 = self.calc_histogram(ImgArray)
			# show both the Image and Histograms
		elif imgSelect == 2:
			ImgArray = cv2.imread("color1.png")
			self.hist2 = self.calc_histogram(ImgArray)
			# show both the Image and Histograms

		# extract the histograms

	def equalize_histogram(self):
		print(self.imgnum)
		self.open_image(3) # show the created image

	def calc_histogram(self, I):
		return None

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