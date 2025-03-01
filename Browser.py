import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl, QPoint

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        # Remove window decorations (title bar, borders)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Simple Qt Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Web view
        self.browser = QWebEngineView(self.central_widget)
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        # Add web view to layout
        self.layout.addWidget(self.browser)

        # Create a transparent overlay for dragging
        self.overlay = DragOverlay(self)
        self.overlay.setGeometry(0, 0, self.width(), 40)  # Only top 40px are draggable
        self.overlay.show()

    def resizeEvent(self, event):
        """Ensure overlay resizes with the main window"""
        self.overlay.setGeometry(0, 0, self.width(), 40)
        super().resizeEvent(event)

class DragOverlay(QWidget):
    """Transparent overlay that captures drag events"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # Accept mouse events
        self._dragging = False
        self._drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
