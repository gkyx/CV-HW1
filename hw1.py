import cv2
import sys
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
		# to be implemented...
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