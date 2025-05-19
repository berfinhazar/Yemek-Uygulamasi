from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
from ana_ekran import AnaEkran
import requests

class YemekAramaSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Yemek Arama")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Öğün Kategorisi
        self.ogun_button = QPushButton("Öğün Seç")
        self.ogun_button.setCheckable(True)
        self.ogun_button.toggled.connect(self.toggle_ogun_choices)
        layout.addWidget(self.ogun_button)

        self.ogun_group = QGroupBox()
        self.ogun_group_layout = QVBoxLayout()
        self.ogun_group_layout.addWidget(QCheckBox("Kahvaltı"))
        self.ogun_group_layout.addWidget(QCheckBox("Öğle Yemeği"))
        self.ogun_group_layout.addWidget(QCheckBox("Akşam Yemeği"))
        self.ogun_group_layout.addWidget(QCheckBox("Atıştırmalık"))
        self.ogun_group_layout.addWidget(QCheckBox("Tatlı"))
        self.ogun_group.setLayout(self.ogun_group_layout)
        self.ogun_group.setVisible(False)

        layout.addWidget(self.ogun_group)

        # Mutfak Türü
        self.mutfak_button = QPushButton("Mutfak Türü Seç")
        self.mutfak_button.setCheckable(True)
        self.mutfak_button.toggled.connect(self.toggle_mutfak_choices)
        layout.addWidget(self.mutfak_button)

        self.mutfak_group = QGroupBox()
        self.mutfak_group_layout = QVBoxLayout()
        for mutfak in ["Türk", "İtalyan", "Meksika", "Çin", "Hindistan", "Fransız", "Akdeniz", "Japon", "İspanyol", "Yunan"]:
            self.mutfak_group_layout.addWidget(QCheckBox(mutfak))
        self.mutfak_group.setLayout(self.mutfak_group_layout)
        self.mutfak_group.setVisible(False)
        layout.addWidget(self.mutfak_group)

        # Alerjen
        self.alerjen_button = QPushButton("Alerjen Seç")
        self.alerjen_button.setCheckable(True)
        self.alerjen_button.toggled.connect(self.toggle_alerjen_choices)
        layout.addWidget(self.alerjen_button)

        self.alerjen_group = QGroupBox()
        self.alerjen_group_layout = QVBoxLayout()
        for alerjen in ["Gluten", "Süt Ürünleri", "Fındık", "Yumurta", "Deniz Ürünleri", "Soya", "Alerjen Şeker", "Buğday", "Fasulye", "Laktoz"]:
            self.alerjen_group_layout.addWidget(QCheckBox(alerjen))
        self.alerjen_group.setLayout(self.alerjen_group_layout)
        self.alerjen_group.setVisible(False)
        layout.addWidget(self.alerjen_group)

        # Tarifleri Getir Butonu
        button_layout = QHBoxLayout()
        self.tarifleri_getir_btn = QPushButton("Tarifleri Getir")
        self.tarifleri_getir_btn.clicked.connect(self.tarifleri_getir_clicked)
        button_layout.addStretch()
        button_layout.addWidget(self.tarifleri_getir_btn, alignment=Qt.AlignRight)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def toggle_ogun_choices(self):
        self.ogun_group.setVisible(self.ogun_button.isChecked())
        self.mutfak_group.setVisible(False)
        self.alerjen_group.setVisible(False)

    def toggle_mutfak_choices(self):
        self.mutfak_group.setVisible(self.mutfak_button.isChecked())
        self.ogun_group.setVisible(False)
        self.alerjen_group.setVisible(False)

    def toggle_alerjen_choices(self):
        self.alerjen_group.setVisible(self.alerjen_button.isChecked())
        self.ogun_group.setVisible(False)
        self.mutfak_group.setVisible(False)

    def tarifleri_getir_clicked(self):
        ogun_map = {
            "Kahvaltı": "breakfast",
            "Öğle Yemeği": "lunch",
            "Akşam Yemeği": "dinner",
            "Atıştırmalık": "snack",
            "Tatlı": "dessert"
        }

        mutfak_map = {
            "Türk": "Turkish",
            "İtalyan": "Italian",
            "Meksika": "Mexican",
            "Çin": "Chinese",
            "Hindistan": "Indian",
            "Fransız": "French",
            "Akdeniz": "Mediterranean",
            "Japon": "Japanese",
            "İspanyol": "Spanish",
            "Yunan": "Greek"
        }

        alerjen_map = {
            "Gluten": "gluten",
            "Süt Ürünleri": "dairy",
            "Fındık": "peanut",
            "Yumurta": "egg",
            "Deniz Ürünleri": "seafood",
            "Soya": "soy",
            "Alerjen Şeker": "sugar",
            "Buğday": "wheat",
            "Fasulye": "bean",
            "Laktoz": "lactose"
        }

        ogun = [ogun_map[cb.text()] for cb in self.ogun_group.findChildren(QCheckBox) if cb.isChecked()]
        mutfak = [mutfak_map[cb.text()] for cb in self.mutfak_group.findChildren(QCheckBox) if cb.isChecked()]
        alerjen = [alerjen_map[cb.text()] for cb in self.alerjen_group.findChildren(QCheckBox) if cb.isChecked()]

        params = {
            "apiKey": "98c8d98ae4dc4e2b87fcf2d008730e99",
            "number": 5
        }
        if ogun:
            params["type"] = ogun[0]
        if mutfak:
            params["cuisine"] = ",".join(mutfak)
        if alerjen:
            params["intolerances"] = ",".join(alerjen)

        print("API İsteği Yapılıyor...")
        print("Parametreler:", params)

        try:
            response = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=params)
            data = response.json()
            print("API Yanıtı:", data)

            tarifler = data.get("results", [])
            print("Tarifler:", tarifler)
            if tarifler:
                print("Tarifler başarıyla alındı.")  # ← Bunu ekledik
                if self.parent:
                   self.parent.show_main_screen(tarifler)
                else:
                    print("Parent tanımlı değil, tarifleri gösteremiyorum.")
            else:
                print("Tarif bulunamadı....")
        except Exception as e:
            print("Bir hata oluştu:", e)

