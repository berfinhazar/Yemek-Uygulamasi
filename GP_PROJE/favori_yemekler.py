from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class FavoriYemekler(QMainWindow):
    def __init__(self, favori_tarifler,sil):
        super().__init__()
        self.favori_tarifler = favori_tarifler
        self.sil=sil
        self.setWindowTitle("Favori Tarifler")
        self.setGeometry(100, 100, 600, 600)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        if not self.favori_tarifler:
            no_favorites_label = QLabel("Henüz favori tarif eklemediniz.")
            self.layout.addWidget(no_favorites_label)
        else:
            for tarif in self.favori_tarifler:
                h_layout = QHBoxLayout()

                tarif_label = QLabel(tarif["title"])
                tarif_label.setStyleSheet("font-size: 14px; font-weight: bold;")
                h_layout.addWidget(tarif_label)

                sil_button = QPushButton("Favorilerden Kaldır")
                sil_button.clicked.connect(lambda _, t=tarif: self.remove_from_favorites(t))
                h_layout.addWidget(sil_button)

                self.layout.addLayout(h_layout)

        self.setCentralWidget(self.central_widget)

    def remove_from_favorites(self, tarif):
        # Favorilerden çıkar
        if tarif in self.favori_tarifler:
            self.favori_tarifler.remove(tarif)

        # Arayüzü güncelle
        self.clear_layout(self.layout)
        self.init_ui()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())
