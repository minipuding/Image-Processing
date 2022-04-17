import PyQt5
import PyQt5.QtWidgets as qw

class MyGraphicsView(qw.QGraphicsView):
    def __init__(self, *__args):
        super().__init__()
        self.moveX = 0
        self.moveY = 0
        self.pressedX = 0
        self.pressedY = 0

        self.setMouseTracking(True)
        # self.myscene = self.scene()

    def mousePressEvent(self, event):
        self.pressedX = event.x()
        self.pressedY = event.y()

    def mouseMoveEvent(self, event):
        self.moveX = event.x()
        self.moveY = event.y()