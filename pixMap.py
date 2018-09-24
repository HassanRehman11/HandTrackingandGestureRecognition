from PyQt5.QtGui import QImage, QPixmap
class Pix:
    @staticmethod
    def display(image,label):
        size = image.shape
        step = image.size / size[0]
        qformat = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()

        label.setPixmap(QPixmap.fromImage(img))
        label.setScaledContents(True)



