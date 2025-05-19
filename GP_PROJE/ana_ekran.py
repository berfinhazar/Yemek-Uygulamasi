import requests
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from favori_yemekler import FavoriYemekler

class AnaEkran(QWidget):
    def __init__(self, tarif_listesi):
        super().__init__()
        self.tarif_listesi = tarif_listesi
        self.favori_tarifler = []

        self.setWindowTitle("Tarifler")
        self.setGeometry(100, 100, 600, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        favoriler_button = QPushButton("Favori Tarifleri Göster")
        favoriler_button.clicked.connect(self.show_favorites)
        layout.addWidget(favoriler_button)

        for tarif in self.tarif_listesi:
            kart = self.create_tarif_card(tarif)
            scroll_layout.addWidget(kart)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def create_tarif_card(self, tarif):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("QFrame { border: 1px solid gray; padding: 10px; margin: 5px; }")

        layout = QHBoxLayout()

        # Tarif görseli varsa göster
        if tarif.get("image"):
            try:
                response = requests.get(tarif["image"])
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                layout.addWidget(image_label)
            except:
                pass

        # Tarif adı
        ad_label = QLabel(tarif["title"])
        ad_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        ad_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(ad_label)

        # Yıldız ikonu (favorilere eklemek için)
        star_button = QPushButton()
        star_button.setIcon(QIcon("ikon/Ekran Resmi 2025-05-03 18.12.52.png"))  # Yıldız ikonunu buraya ekle
        star_button.clicked.connect(lambda: self.add_to_favorites(tarif))
        star_button.setIconSize(QSize(50, 50))
        layout.addWidget(star_button)

        # Detayları gizle
        detaylar_layout = QVBoxLayout()

        # Detayları dinamik olarak al
        tarif_detay = self.get_tarif_detay(tarif["id"])

        if tarif_detay:
            malzemeler_label = QLabel("Malzemeler: " + ", ".join([ingredient["name"] for ingredient in tarif_detay["extendedIngredients"]]))
            malzemeler_label.setWordWrap(True)
            tarif_nasil_label = QLabel("Nasıl Yapılır: " + tarif_detay.get("instructions", "Açıklama bulunmuyor."))
            tarif_nasil_label.setWordWrap(True)

            detaylar_layout.addWidget(malzemeler_label)
            detaylar_layout.addWidget(tarif_nasil_label)

        detaylar_widget = QWidget()
        detaylar_widget.setLayout(detaylar_layout)
        detaylar_widget.setVisible(False)

        # Tarife tıklanabilir alan
        ad_label.mousePressEvent = lambda event: self.toggle_details(detaylar_widget)

        layout.addWidget(detaylar_widget)

        card.setLayout(layout)
        return card

    def get_tarif_detay(self, tarif_id):
        url = f"https://api.spoonacular.com/recipes/{tarif_id}/information"
        params = {
            'apiKey': ' be4493ff85dd4f0b8344c697f160823c',
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Detaylar alınırken hata oluştu: {response.status_code}")
            return None

    def toggle_details(self, detaylar_widget):
        detaylar_widget.setVisible(not detaylar_widget.isVisible())

    def add_to_favorites(self, tarif):
        if tarif not in self.favori_tarifler:  # Tarif zaten favorilerde değilse
            self.favori_tarifler.append(tarif)  # Favorilere ekle
            success = self.show_favorite_message(tarif['title'])
            if success:
                print(f"{tarif['title']} favorilere eklendi.")
        else:
            print(f"{tarif['title']} zaten favorilerde.")
    def remove_from_favorites(self, tarif):
        if tarif in self.favori_tarifler:
            self.favori_tarifler.remove(tarif)
            print(f"{tarif['title']} favorilerden kaldırıldı.")
        else:
            print(f"{tarif['title']} favorilerde bulunmuyor.")

    def show_favorite_message(self, tarif_title):
        # Favorilere eklenme mesajını göstermek için bir QMessageBox kullanıyoruz
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"{tarif_title} favorilere eklendi.")
        msg.setWindowTitle("Favori Ekleme")
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec_() == QMessageBox.Ok
    def show_favorites(self):

    # Favori tarifler sayfası aç
        if hasattr(self, 'favori_ekran') and self.favori_ekran.isVisible():
           self.favori_ekran.close()  # Eğer favori ekran zaten açıksa, kapatıyoruz.

        self.favori_ekran = FavoriYemekler(self.favori_tarifler, self.remove_from_favorites)
        self.favori_ekran.show()