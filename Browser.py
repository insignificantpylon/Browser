import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QHBoxLayout, QPushButton, QLineEdit
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl, QPoint

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Simple Qt Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.browser = QWebEngineView(self.central_widget)
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.update_url_bar)
        
        self.create_navigation_bar()
        
        self.layout.addWidget(self.browser)
        
        self.overlay = DragOverlay(self)
        self.overlay.setGeometry(0, 0, self.width(), 40)
        self.overlay.show()

    def create_navigation_bar(self):
        nav_bar = QWidget(self.central_widget)
        nav_bar.setFixedHeight(40)  # Reduce height to match button height
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(5, 0, 5, 0)
        nav_layout.setSpacing(5)
        
        self.back_button = QPushButton("◀", self)
        self.back_button.setFixedSize(30, 30)
        self.back_button.clicked.connect(self.browser.back)
        
        self.reload_button = QPushButton("⟳", self)
        self.reload_button.setFixedSize(30, 30)
        self.reload_button.clicked.connect(self.browser.reload)
        
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.load_url)
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.url_bar, 1)
        
        self.layout.insertWidget(0, nav_bar)  # Ensure it's at the very top
    
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))
    
    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())
    
    def resizeEvent(self, event):
        self.overlay.setGeometry(0, 0, self.width(), 40)
        super().resizeEvent(event)

class DragOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self._dragging = False
        self._drag_position = QPoint()
        self.setFixedHeight(40)  # Match the height of navigation bar

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
