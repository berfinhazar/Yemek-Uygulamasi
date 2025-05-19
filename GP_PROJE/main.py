from PyQt5.QtWidgets import QApplication, QMainWindow

from ana_ekran import AnaEkran
from kullanici_girisi import KullaniciGirisi
from yemek_arama import YemekAramaSayfasi
from tarif_detayi import TarifDetayi
import sys

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yemek Tarif Uygulaması")
        self.show_login_form()

    def show_login_form(self):
        self.login_form = KullaniciGirisi()
        self.login_form.giris_basarili.connect(self.show_main_screen)
        self.setCentralWidget(self.login_form)

    def show_main_screen(self, tarifler=None):
        if tarifler:
            self.main_screen = AnaEkran(tarifler)
            self.setCentralWidget(self.main_screen)
        else:
            self.main_screen = YemekAramaSayfasi(self)
        self.setCentralWidget(self.main_screen)


    def show_recipe_details(self):
        self.recipe_details = TarifDetayi()
        self.setCentralWidget(self.recipe_details)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
