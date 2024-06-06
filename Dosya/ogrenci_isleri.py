from PyQt5.QtWidgets import *
from ogrenci_isleri_python import Ui_Form
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtWidgets import QLineEdit
import ogrenci_isleri_sql
import sys


class ogrenci_isleriPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ogrenci_isleriform = Ui_Form()
        self.ogrenci_isleriform.setupUi(self)
        self.ogrenci_isleriform.groupBox_kayit.hide()
        self.ogrenci_isleriform.groupBox_tablo.show()
        self.ogrenci_isleriform.tableWidget_tablo.setFocusPolicy(Qt.ClickFocus)
        self.satir_index = 0
        self.ogrenci_isleriform.pushButton_ogruyeekrani.clicked.connect(self.kayitol)
        self.ogrenci_isleriform.pushButton_geridon.clicked.connect(self.geridon)
        self.ogrenci_isleriform.pushButton_onayla.clicked.connect(self.ogrekle)
        self.ogrenci_isleriform.pushButton_ogrsil.clicked.connect(self.ogrsil)
        self.ogrenci_isleriform.tableWidget_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        current_date = QDate.currentDate()
        self.ogrenci_isleriform.DateEdit_tarih.setDate(current_date)
        self.ogrenci_isleriform.DateEdit_tarih.setFocusPolicy(Qt.NoFocus)
        self.ogrenci_isleriform.pushButton_cikis.clicked.connect(self.exit)
    
        self.TabloyaOgrencileriYerlestir()
        self.style = """
            QLabel {
                font-weight: bold;
                border: none; /* Çerçeveyi kaldırmak için */
                color: maroon;
            }
        """
        self.style2 = """
            QLabel {
                font-weight: bold;
                border: none; /* Çerçeveyi kaldırmak için */
                color: green;
            }
        """
    def ogrsil(self):
        secilisatir = self.ogrenci_isleriform.tableWidget_tablo.currentRow()
        if secilisatir != -1:
            ogrencino = self.ogrenci_isleriform.tableWidget_tablo.item(secilisatir, 2).text()
            print("Öğrenci numarası:", ogrencino) 
            satir_veri = False
            for sutun in range(self.ogrenci_isleriform.tableWidget_tablo.columnCount()):
                if self.ogrenci_isleriform.tableWidget_tablo.item(secilisatir, sutun) is not None:
                    if self.ogrenci_isleriform.tableWidget_tablo.item(secilisatir, sutun).text() != "":
                        satir_veri = True
                        break
            if satir_veri:
                self.ogrenci_isleriform.tableWidget_tablo.removeRow(secilisatir)
                ogrenci_isleri_sql.OgrenciSil(ogrencino)
                self.ogrenci_isleriform.label_bilgilendirme_2.setStyleSheet(self.style2)
                self.ogrenci_isleriform.label_bilgilendirme_2.setText("Öğrenci Başarıyla Silindi.")
                QTimer.singleShot(3000, self.clearText3)
            else:
                self.ogrenci_isleriform.label_bilgilendirme_2.setStyleSheet(self.style)
                self.ogrenci_isleriform.label_bilgilendirme_2.setText("Seçili satır boş.")
                QTimer.singleShot(3000, self.clearText3)

    def kayitol(self):
        if self.ogrenci_isleriform.groupBox_tablo.isVisible():
            self.ogrenci_isleriform.groupBox_tablo.hide()
        self.ogrenci_isleriform.groupBox_kayit.show()

    def ogrekle(self):
        if self.ogrenci_isleriform.lineEdit_ad.text() != "" and \
        self.ogrenci_isleriform.lineEdit_soyad.text() != "" and \
        self.ogrenci_isleriform.lineEdit_ogrencino.text() != "" and \
        self.ogrenci_isleriform.lineEdit_sifre.text() != "" and \
        self.ogrenci_isleriform.lineEdit_telefonno.text() != "" and \
        self.ogrenci_isleriform.lineEdit_eposta.text() != "" and \
        self.ogrenci_isleriform.lineEdit_fakulte.text() != "" and \
        self.ogrenci_isleriform.lineEdit_bolum.text() != "" and \
        self.ogrenci_isleriform.lineEdit_sinif.text() != "":
            ad = self.ogrenci_isleriform.lineEdit_ad.text()
            soyad = self.ogrenci_isleriform.lineEdit_soyad.text()
            ogrencino = self.ogrenci_isleriform.lineEdit_ogrencino.text()
            sifre = self.ogrenci_isleriform.lineEdit_sifre.text()
            telefonno = self.ogrenci_isleriform.lineEdit_telefonno.text()
            eposta = self.ogrenci_isleriform.lineEdit_eposta.text()
            fakulte = self.ogrenci_isleriform.lineEdit_fakulte.text()
            bolum = self.ogrenci_isleriform.lineEdit_bolum.text()
            sinif = self.ogrenci_isleriform.lineEdit_sinif.text()
            adsoyad = ad + " " + soyad
            ogrtarihi = self.ogrenci_isleriform.DateEdit_tarih.date().toString("dd.MM.yyyy")
            current_date = QDate.currentDate().toString("yyyy-MM-dd")
            print(ogrtarihi)
            print(adsoyad)
            ogrenci_isleri_sql.OgrenciEkle(ogrencino, ad, soyad, sifre, eposta, telefonno, current_date, fakulte, bolum, sinif)
            self.TabloyaOgrencileriYerlestir()
            self.satir_index += 1
            self.ogrenci_isleriform.label_bilgilendirme.setStyleSheet(self.style2)
            self.ogrenci_isleriform.label_bilgilendirme.setText("Öğrenci Başarıyla Kaydedildi.")
            QTimer.singleShot(3000,self.clearText)           
        else:
            self.ogrenci_isleriform.label_bilgilendirme.setStyleSheet(self.style)
            self.ogrenci_isleriform.label_bilgilendirme.setText("Bilgiler eksiksiz girilmek zorundadır.")
            QTimer.singleShot(3000,self.clearText2)

    def clearText(self):
        self.ogrenci_isleriform.lineEdit_ad.setText("")
        self.ogrenci_isleriform.lineEdit_soyad.setText("")
        self.ogrenci_isleriform.lineEdit_ogrencino.setText("")
        self.ogrenci_isleriform.lineEdit_sifre.setText("")
        self.ogrenci_isleriform.lineEdit_telefonno.setText("")
        self.ogrenci_isleriform.lineEdit_eposta.setText("")
        self.ogrenci_isleriform.lineEdit_fakulte.setText("")
        self.ogrenci_isleriform.lineEdit_bolum.setText("")
        self.ogrenci_isleriform.lineEdit_sinif.setText("")
        self.ogrenci_isleriform.label_bilgilendirme.setText("")
    def clearText2(self):
        self.ogrenci_isleriform.label_bilgilendirme.setText("")
    def clearText3(self):
        self.ogrenci_isleriform.label_bilgilendirme_2.setText("")
    
    def geridon(self):
        if self.ogrenci_isleriform.groupBox_kayit.isVisible():
            self.ogrenci_isleriform.groupBox_kayit.hide()
        self.ogrenci_isleriform.groupBox_tablo.show()

    def TabloyaOgrencileriYerlestir(self):
        ogrenciler = ogrenci_isleri_sql.OgrencileriGetir()
        table = self.ogrenci_isleriform.tableWidget_tablo
        table.setRowCount(len(ogrenciler))
        for i, ogrenci in enumerate(ogrenciler):
            for j in range(len(ogrenci)):
                item = QTableWidgetItem(str(ogrenci[j]))
                table.setItem(i, j, item)
    def exit(self):
        sys.exit()
