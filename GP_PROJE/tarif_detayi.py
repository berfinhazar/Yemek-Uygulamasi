from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class TarifDetayi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarif Detayları")


        self.label_details = QLabel("Tarifin Detayları:", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_details)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
