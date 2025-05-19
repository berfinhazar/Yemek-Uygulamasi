from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class KullaniciGirisi(QWidget):
    giris_basarili = pyqtSignal()  # sinyal tanımı

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap / Kaydol")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = QPushButton("Giriş Yap", self)
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Kaydol", self)
        self.register_btn.clicked.connect(self.register_user)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def check_login(self):
        username = self.username.text()
        password = self.password.text()

        if username and password:
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.giris_basarili.emit()  # Sadece bir kez sinyal gönder
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")

    def register_user(self):
        QMessageBox.information(self, "Kayıt", "Kayıt ekranı açılacak!")
