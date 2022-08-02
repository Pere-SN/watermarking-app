from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QFileDialog, QLineEdit
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon, QFont
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Watermark-App")
        self.setWindowIcon(QIcon('image.png'))
        self.setFixedSize(640, 640)

        # Button
        btn_image_selector = QPushButton("Select Image", self)
        btn_image_selector.setGeometry(QRect(40, 570, 140, 41))
        btn_image_selector.clicked.connect(self.get_image)
        btn_image_selector.setStyleSheet("background-color: CornflowerBlue; font: bold")

        btn_apply_watermark = QPushButton("Apply", self)
        btn_apply_watermark.setGeometry(QRect(440, 560, 150, 61))
        btn_apply_watermark.clicked.connect(self.apply_watermark)
        btn_apply_watermark.setStyleSheet("background-color: LightGreen; font: bold")

        # Label
        self.label_watermark = QLineEdit(self, placeholderText="Watermark Text")
        self.label_watermark.setGeometry(QRect(200, 570, 140, 41))

        # QPixmap
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap(''))
        self.image.resize(640, 550)
        self.image.setAlignment(Qt.AlignCenter)

        # QImage
        self.image_to_modify = QImage('')

    def get_image(self):
        fname = QFileDialog(self)
        fname.setFileMode(QFileDialog.AnyFile)
        fname.setNameFilter("Images (*.png *.xpm *.jpg)")
        self.image.clear()
        if fname.exec():
            filename = fname.selectedFiles()
            self.image.setPixmap(QPixmap(filename[0]).scaled(640, 550, Qt.KeepAspectRatio))
            self.image_to_modify = QImage(filename[0])

    def apply_watermark(self):
        image = self.image_to_modify

        painter = QPainter()
        painter.begin(image)
        painter.setOpacity(0.2)
        painter.setPen(Qt.white)

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setItalic(True)
        font.setPointSize(image.width()/6)
        painter.setFont(font)
        painter.drawText(image.rect(), Qt.AlignCenter, self.label_watermark.text())
        painter.end()

        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Image", r"C:", "Images (*.png *.xpm *.jpg)", options=options
        )

        if filename:
            image.save(f'{filename}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

