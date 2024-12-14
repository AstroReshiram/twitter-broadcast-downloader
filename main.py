import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from downloader.utils import *
from selenium import webdriver

import validators

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitter Broadcast Downloader")

        # Center the window on the screen
        screen_size = QApplication.primaryScreen().availableGeometry()

        width = 350
        height = 50
        self.setGeometry((screen_size.width() - width) // 2, (screen_size.height() - height) // 2, width, height)
        
        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        # Create a text box
        self.text_box = QLineEdit(self)
        self.download_button = QPushButton("Download", self)
        self.download_button.setFixedWidth(self.width() // 2) 
        self.download_button.clicked.connect(self.download)

        self.label = QLabel("hiii")

        layout.addWidget(self.text_box)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.download_button, alignment=Qt.AlignCenter)

    def download(self):
        url = self.text_box.text()
        url = url if "http://" in url or "https://" in url else "https://" + url
        result = validators.url(url)

        if result and "twitter.com" in url:
            self.label.setText("Downloading!")
            self._run_download(url)
        else:
            self.label.setText("Not a valid twitter url!!!!!")

    def _run_download(self, url):
        driver = webdriver.Chrome()

        driver.get(url)
        driver.execute_script(open("downloader/listener.js", "r").read())

        data = ""

        while not data:
            for i in driver.get_log("browser"):
                if (
                    "message" in i
                    and "source" in i
                    and i["source"] == "console-api"
                    and ".m3u8" in i["message"]
                ):
                    data = i["message"]

        driver.quit()

        # file = codecs.open("temp", "w", "utf-8")
        # file.write(data)
        # file.close()

        # data = open("temp", "r", encoding="utf-8").read()
        m3u8_url = extract_m3u8_url(data)

        download(m3u8_url)
        # remove_file("temp")
        self.label.setText("Done!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
