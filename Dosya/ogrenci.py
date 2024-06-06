from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from ogrenci_python import Ui_MainWindow_ogrenci
from PyQt5.QtGui import QColor, QFont,QIcon
from PyQt5.QtCore import QTimer
import sys
import ogrenci_sql
    
class ogrenciPage(QMainWindow):
    def __init__(self, ogr_no) -> None:
        super().__init__()
        self.ogr_no = ogr_no
        

        ogr_ad = ogrenci_sql.OgrAdGet(self.ogr_no)
        ogr_soyad = ogrenci_sql.OgrSoyadGet(self.ogr_no)
        ogr_mail = str(ogrenci_sql.OgrMailGet(self.ogr_no)[0])
        ogr_fakulte = str(ogrenci_sql.OgrFakulteGet(self.ogr_no)[0])
        global ogr_kayit_t
        ogr_kayit_t = ogrenci_sql.OgrKayitGet(self.ogr_no)
        global kesinMi
        kesinMi = ogrenci_sql.KesinlestirGet(self.ogr_no)
        ogr_ad_soyad = f"{ogr_ad[0]} {ogr_soyad[0]}" if ogr_ad and ogr_soyad else ""
        self.ogrenciform = Ui_MainWindow_ogrenci()
        self.ogrenciform.setupUi(self)
        font = QFont("Microsoft Yahei UI Light")
        font.setPointSize(16)
        self.sifre = "1"
        self.ogrenciform.groupBox_derskayit.hide()
        self.ogrenciform.groupBox_NotListesi.hide()
        self.ogrenciform.groupBox_sifredegistir.hide()
        self.ogrenciform.groupBox_AkademikTakvim.hide()
        self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
        self.ogrenciform.label_blok.hide()
        self.ogrenciform.label_bilgilendirme.hide()
        self.dersler = []
        self.dersler1 = ogrenci_sql.DersGetir()
        self.ogrenciform.lineEdit_eskisifre.setFocusPolicy(Qt.ClickFocus)
        self.ogrenciform.lineEdit_yenisifre1.setFocusPolicy(Qt.ClickFocus)
        self.ogrenciform.lineEdit_yenisifre2.setFocusPolicy(Qt.ClickFocus)
        if kesinMi == True:
            self.ogrenciform.tableWidget_devamsizlikbilgisi.hide() 
            self.ogrenciform.tableWidget_notlarim.hide()
        self.ogrenciform.groupBox_anamenu.show()
        self.ogrenciform.tableWidget_kayit.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ogrenciform.tableWidget_kesinlesendersler.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ogrenciform.tableWidget_devamsizlikbilgisi.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ogrenciform.tableWidget_notlarim.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ogrenciform.listWidget_menu.itemClicked.connect(self.item_clicked)
        self.ders_sayaci = 0
        self.ogrenciform.pushButton_kesinlestir.setEnabled(False)
        self.eskisifre_clicked = False
        self.yenisifre1_clicked = False
        self.yenisifre2_clicked = False
        font2 = QFont("Microsoft YaHei UI Light")
        font2.setPointSize(25)
        self.ogrenciform.lineEdit_eskisifre.setFont(font2)
        font2.setPointSize(25)
        self.ogrenciform.lineEdit_yenisifre1.setFont(font2)
        font2.setPointSize(25)
        self.ogrenciform.lineEdit_yenisifre2.setFont(font2)
        self.ogrenciform.lineEdit_eskisifre.setEchoMode(QLineEdit.Normal)
        self.ogrenciform.lineEdit_yenisifre1.setEchoMode(QLineEdit.Normal)
        self.ogrenciform.lineEdit_yenisifre2.setEchoMode(QLineEdit.Normal)
        self.ogrenciform.lineEdit_eskisifre.setText("Mevcut şifre")
        self.ogrenciform.lineEdit_yenisifre1.setText("Yeni şifre")
        self.ogrenciform.lineEdit_yenisifre2.setText("Yeni şifreyi tekrar yaz")
        self.ogrenciform.lineEdit_eskisifre.mousePressEvent = self.selected_eskisifre
        self.ogrenciform.lineEdit_yenisifre1.mousePressEvent = self.selected_yenisifre1
        self.ogrenciform.lineEdit_yenisifre2.mousePressEvent = self.selected_yenisifre2
        self.ogrenciform.pushButton_sifredegistir.clicked.connect(self.sifreDegistir) 
        self.ogrenciform.pushButton_numara.setText("Öğrenci Numarası:"+str(self.ogr_no))  
        self.ogrenciform.pushButton_isimsoyisim.setText(ogr_ad_soyad)  
        self.ogrenciform.pushButton_email.setText(ogr_mail)  
        self.ogrenciform.pushButton_fakulte.setText(ogr_fakulte)  
        self.ders_bilgilerini_tabloya_ekle()   
        self.devamsizlik_bilgilerini_tabloya_ekle()
        self.NotlarıGoster()
        agno = self.AgnoHesapla()
        self.ogrenciform.pushButton_kayittarihi.setText("Kayıt Tarihi:" + ogr_kayit_t + "\n"+"AGNO:" + str(agno)) 
 
    def devamsizlik_bilgilerini_tabloya_ekle(self):
        ogrenci = self.ogr_no
        devamsiz = ogrenci_sql.DevamsizlikGetir(ogrenci)
        dersler = ogrenci_sql.DersGetir()
        row_count = self.ogrenciform.tableWidget_devamsizlikbilgisi.rowCount()
        for i, ders in enumerate(devamsiz):
            if i < row_count:
                ders_devamsiz = ders[1]
                cellDD = QTableWidgetItem(f"{ders_devamsiz}")
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 4, cellDD)
        for i in range(row_count):
            if i >= len(devamsiz):  
                cellDD = QTableWidgetItem("Girilmedi")
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 4, cellDD)
        for i, ders in enumerate(dersler):
            if i < row_count:
                ders_kodu = ders[0]
                ders_adi = ders[1]
                ders_kredi = ders[2]
                ders_sinif = ders[3]
                cellDK = QTableWidgetItem(f"{ders_kodu}")
                cellDA = QTableWidgetItem(f"{ders_adi}")
                cellDKKredi = QTableWidgetItem(f"{ders_kredi}")
                cellDS = QTableWidgetItem(f"{ders_sinif}")
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 0, cellDK)
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 1, cellDA)
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 2, cellDKKredi)
                self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 3, cellDS)

    def NotlarıGoster(self):
        ogrenci_no = self.ogr_no
        dersler = ogrenci_sql.DersGetir()
        for i, ders in enumerate(dersler):
            ders_kodu = ders[0]
            vize_notu, final_notu = ogrenci_sql.NotGetir(ogrenci_no, ders_kodu)
            if vize_notu != "Girilmedi" and final_notu != "Girilmedi":
                sDurum = "Sonuçlandırıldı"
                ort_not = self.OrtHesapla(vize_notu,final_notu)
                durum = "Geçti" if ort_not >= 60 else "Kaldı"
            else:
                sDurum = "Sonuçlandırılmadı"
                vize_notu = final_notu = "Girilmedi"
                ort_not = durum = "Girilmedi"
            s_durum = QTableWidgetItem(f"{sDurum}")
            s_durum.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 2, s_durum)
            item_vize = QTableWidgetItem(f"{vize_notu}")
            item_vize.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 3, item_vize)
            item_final = QTableWidgetItem(f"{final_notu}")
            item_final.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 4, item_final)
            item_ort = QTableWidgetItem(f"{ort_not}")
            item_ort.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 5, item_ort)
            item_durum = QTableWidgetItem(f"{durum}")
            item_durum.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 6, item_durum)
            if kesinMi == False:
                item_dersKodu = QTableWidgetItem(f"{ders_kodu}")
                item_dersKodu.setTextAlignment(Qt.AlignCenter)
                self.ogrenciform.tableWidget_kesinlesendersler.setItem(0, i, item_dersKodu)
                self.ogrenciform.label_ogrencikesinlestirme.setText("Öğrenci Kesinleştirme Durumu : Kesinleştirildi")

    def NotlarıGosterKesin(self):
        ogrenci_no = self.ogr_no
        dersler = ogrenci_sql.DersGetir()
        for i, ders in enumerate(dersler):
            ders_kodu = ders[0]
            vize_notu, final_notu = ogrenci_sql.NotGetir(ogrenci_no, ders_kodu)
            if vize_notu != "Girilmedi" and final_notu != "Girilmedi":
                sDurum = "Sonuçlandırıldı"
                ort_not = self.OrtHesapla(vize_notu,final_notu)
                durum = "Geçti" if ort_not >= 60 else "Kaldı"
            else:
                sDurum = "Sonuçlandırılmadı"
                vize_notu = final_notu = "Girilmedi"
                ort_not = durum = "Girilmedi"
            s_durum = QTableWidgetItem(f"{sDurum}")
            s_durum.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 2, s_durum)
            item_vize = QTableWidgetItem(f"{vize_notu}")
            item_vize.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 3, item_vize)
            item_final = QTableWidgetItem(f"{final_notu}")
            item_final.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 4, item_final)
            item_ort = QTableWidgetItem(f"{ort_not}")
            item_ort.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 5, item_ort)
            item_durum = QTableWidgetItem(f"{durum}")
            item_durum.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 6, item_durum)
            item_dersKodu = QTableWidgetItem(f"{ders_kodu}")
            item_dersKodu.setTextAlignment(Qt.AlignCenter)
            self.ogrenciform.tableWidget_kesinlesendersler.setItem(0, i, item_dersKodu)

    def ders_bilgilerini_tabloya_ekle(self):
        dersler = ogrenci_sql.DersGetir()
        self.ders_adi_belirle()
        for i, ders in enumerate(dersler):
            ders_kodu = ders[0]
            ders_adi = ders[1]
            ders_kredi = ders[2]
            ders_sinif = ders[3]
            ders_alis = ders[4]
            cellDK = QTableWidgetItem(f"{ders_kodu}")
            cellDA = QTableWidgetItem(f"{ders_adi}")
            cellDKKredi = QTableWidgetItem(f"{ders_kredi}")
            cellDS = QTableWidgetItem(f"{ders_sinif}")
            cellDAl = QTableWidgetItem(f"{ders_alis}")
            self.ogrenciform.tableWidget_kayit.setItem(i, 0, cellDK)
            self.ogrenciform.tableWidget_kayit.setItem(i, 1, cellDA)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 1, cellDA)
            self.ogrenciform.tableWidget_kayit.setItem(i, 2, cellDKKredi)
            self.ogrenciform.tableWidget_kayit.setItem(i, 3, cellDS)
            self.ogrenciform.tableWidget_kayit.setItem(i, 4, cellDAl)
            if kesinMi == False:
                self.ogrenciform.tableWidget_kesinlesendersler.setItem(0, i, cellDK)

    def selected_eskisifre(self, event):
        if not self.eskisifre_clicked:
            font3 = QFont()
            font3.bold()
            self.ogrenciform.lineEdit_eskisifre.setFont(font3)
            self.ogrenciform.lineEdit_eskisifre.setText("")
            self.ogrenciform.lineEdit_eskisifre.setEchoMode(QLineEdit.Password)
            self.eskisifre_clicked = True
        
    def selected_yenisifre1(self, event):
        if not self.yenisifre1_clicked:
            font4 = QFont()
            font4.bold()
            self.ogrenciform.lineEdit_eskisifre.setFont(font4)
            self.ogrenciform.lineEdit_yenisifre1.setText("")
            self.ogrenciform.lineEdit_yenisifre1.setEchoMode(QLineEdit.Password)
            self.yenisifre1_clicked = True
            
    def selected_yenisifre2(self, event):
        if not self.yenisifre2_clicked:
            font5 = QFont()
            font5.bold()
            self.ogrenciform.lineEdit_eskisifre.setFont(font5)
            self.ogrenciform.lineEdit_yenisifre2.setText("")
            self.ogrenciform.lineEdit_yenisifre2.setEchoMode(QLineEdit.Password)
            self.yenisifre2_clicked = True
    
    def sifreDegistir(self):
        ogrenci_no = self.ogr_no
        yeni_sifre = self.ogrenciform.lineEdit_yenisifre1.text()
        yeni_sifre_tekrar = self.ogrenciform.lineEdit_yenisifre2.text()
        eski_sifre = self.ogrenciform.lineEdit_eskisifre.text()
        if yeni_sifre == yeni_sifre_tekrar:
            if ogrenci_sql.SifreAyniMi(ogrenci_no, eski_sifre): 
                if self.ogrenciform.checkBox_girisekraninadon.isChecked():
                    ogrenci_sql.SifreDegistir(ogrenci_no, eski_sifre, yeni_sifre)
                    self.ogrenciform.label_sifreguncellendi.setStyleSheet("QLabel { color: #008000; font-size: 16px; font-weight: bold; }")
                    self.ogrenciform.label_sifreguncellendi.setText("Şifreniz başarıyla güncellendi.")
                    QTimer.singleShot(3000,self.clearText2)
                else:
                    ogrenci_sql.SifreDegistir(ogrenci_no, eski_sifre, yeni_sifre)
                    self.ogrenciform.label_sifreguncellendi.setStyleSheet("QLabel { color: #008000; font-size: 16px; font-weight: bold; }")
                    self.ogrenciform.label_sifreguncellendi.setText("Şifreniz başarıyla güncellendi.")
                    QTimer.singleShot(3000, self.clearText)
            else:
                self.ogrenciform.label_sifreguncellendi.setStyleSheet("QLabel { color: maroon; font-size: 16px; font-weight: bold; }")
                self.ogrenciform.label_sifreguncellendi.setText("Eski şifren yanlış girildi. Lütfen tekrar girin.")
                QTimer.singleShot(3000, self.clearText) 
        else:
            self.ogrenciform.label_sifreguncellendi.setStyleSheet("QLabel { color: maroon; font-size: 16px; font-weight: bold; }")
            self.ogrenciform.label_sifreguncellendi.setText("Yeni şifreler eşleşmiyor. Yeni şifreyi tekrar girin.") 
            QTimer.singleShot(3000, self.clearText)
 
    def clearText(self):
        self.ogrenciform.label_sifreguncellendi.setText("")

    def clearText2(self):
        sys.exit()

    def OrtHesapla(self, vize=0, final=0):
        vize = float(vize)
        final = float(final)
        ortalama = (vize * 0.4) + (final * 0.6)
        return ortalama

    def ders_adi_belirle(self):
        dersler = ogrenci_sql.DersGetir()
        for i, ders in enumerate(dersler):
            ders_kodu = ders[0]
            ders_adi = ders[1]
            cellDA = QTableWidgetItem(f"{ders_adi}")
            cellDK = QTableWidgetItem(f"{ders_kodu}")
            self.ogrenciform.tableWidget_notlarim.setItem(i, 1, cellDA)
            self.ogrenciform.tableWidget_notlarim.setItem(i, 0, cellDK)

    def item_clicked(self,item):
        print("Tıklanan öğe:", item.text()) 
        if item.text() == "Ana Menü":
            if self.ogrenciform.groupBox_derskayit.isVisible():
                self.ogrenciform.groupBox_derskayit.hide()
            if self.ogrenciform.groupBox_NotListesi.isVisible():
                self.ogrenciform.groupBox_NotListesi.hide()
            if self.ogrenciform.groupBox_sifredegistir.isVisible():
                self.ogrenciform.groupBox_sifredegistir.hide()
            if self.ogrenciform.groupBox_Devamsizlikdurumu.isVisible():
                self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
            if self.ogrenciform.groupBox_AkademikTakvim.isVisible():
                self.ogrenciform.groupBox_AkademikTakvim.hide()
            self.ogrenciform.groupBox_anamenu.show()
        if item.text() == "Ders Kayıt":
            if self.ogrenciform.groupBox_anamenu.isVisible():
                self.ogrenciform.groupBox_anamenu.hide()
            if self.ogrenciform.groupBox_NotListesi.isVisible():
                self.ogrenciform.groupBox_NotListesi.hide()
            if self.ogrenciform.groupBox_sifredegistir.isVisible():
                self.ogrenciform.groupBox_sifredegistir.hide()
            if self.ogrenciform.groupBox_Devamsizlikdurumu.isVisible():
                self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
            if self.ogrenciform.groupBox_AkademikTakvim.isVisible():
                self.ogrenciform.groupBox_AkademikTakvim.hide()
            self.ogrenciform.groupBox_derskayit.show()
            if kesinMi == True:
                self.ogrenciform.pushButton_1.clicked.connect(self.Ders1)
                self.ogrenciform.pushButton_2.clicked.connect(self.Ders2)
                self.ogrenciform.pushButton_3.clicked.connect(self.Ders3)
                self.ogrenciform.pushButton_4.clicked.connect(self.Ders4)
                self.ogrenciform.pushButton_5.clicked.connect(self.Ders5)
                self.ogrenciform.pushButton_6.clicked.connect(self.Ders6)
                self.ogrenciform.pushButton_7.clicked.connect(self.Ders7)
                self.ogrenciform.pushButton_8.clicked.connect(self.Ders8)
                self.ogrenciform.pushButton_kesinlestir.clicked.connect(self.kesinlestir)
            else:
                self.ogrenciform.pushButton_1.setDisabled(True)                
                self.ogrenciform.pushButton_2.setDisabled(True)
                self.ogrenciform.pushButton_3.setDisabled(True)
                self.ogrenciform.pushButton_4.setDisabled(True)
                self.ogrenciform.pushButton_5.setDisabled(True)
                self.ogrenciform.pushButton_6.setDisabled(True)
                self.ogrenciform.pushButton_7.setDisabled(True)
                self.ogrenciform.pushButton_8.setDisabled(True)
        if item.text() == "Not Listesi":
            if self.ogrenciform.groupBox_anamenu.isVisible():
                self.ogrenciform.groupBox_anamenu.hide()
            if self.ogrenciform.groupBox_derskayit.isVisible():
                self.ogrenciform.groupBox_derskayit.hide()
            if self.ogrenciform.groupBox_sifredegistir.isVisible():
                self.ogrenciform.groupBox_sifredegistir.hide()
            if self.ogrenciform.groupBox_Devamsizlikdurumu.isVisible():
                self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
            if self.ogrenciform.groupBox_AkademikTakvim.isVisible():
                self.ogrenciform.groupBox_AkademikTakvim.hide()
            self.ogrenciform.groupBox_NotListesi.show()
            if self.ogrenciform.pushButton_kesinlestir.text() == "Kesinleştirildi":
                self.ogrenciform.tableWidget_notlarim.show()
                self.ogrenciform.label_notlistesi.setText("Not Durumu")
                self.ogrenciform.label_blok.show()      
                for i, ders in enumerate(self.dersler):
                    item = QTableWidgetItem(ders)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ogrenciform.tableWidget_notlarim.setItem(i, 0, item)
                self.ogrenciform.label_bilgilendirme.show()                
        if item.text() == "Akademik Takvim":
            if self.ogrenciform.groupBox_anamenu.isVisible():
                self.ogrenciform.groupBox_anamenu.hide()
            if self.ogrenciform.groupBox_derskayit.isVisible():
                self.ogrenciform.groupBox_derskayit.hide()
            if self.ogrenciform.groupBox_NotListesi.isVisible():
                self.ogrenciform.groupBox_NotListesi.hide()
            if self.ogrenciform.groupBox_Devamsizlikdurumu.isVisible():
                self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
            if self.ogrenciform.groupBox_sifredegistir.isVisible():
                self.ogrenciform.groupBox_sifredegistir.hide()          
            self.ogrenciform.groupBox_AkademikTakvim.show()
        if item.text() == "Şikayet Kutusu":
            pass     
        if item.text() == "Devamsızlık Durumu":
            if self.ogrenciform.groupBox_anamenu.isVisible():
                self.ogrenciform.groupBox_anamenu.hide()
            if self.ogrenciform.groupBox_derskayit.isVisible():
                self.ogrenciform.groupBox_derskayit.hide()
            if self.ogrenciform.groupBox_NotListesi.isVisible():
                self.ogrenciform.groupBox_NotListesi.hide()
            if self.ogrenciform.groupBox_sifredegistir.isVisible():
                self.ogrenciform.groupBox_sifredegistir.hide()
            self.ogrenciform.groupBox_Devamsizlikdurumu.show()
            if self.ogrenciform.groupBox_AkademikTakvim.isVisible():
                self.ogrenciform.groupBox_AkademikTakvim.hide()
            if self.ogrenciform.pushButton_kesinlestir.text() == "Kesinleştirildi":
                self.ogrenciform.tableWidget_devamsizlikbilgisi.show()
                self.ogrenciform.label_devamsizlikdurumu.setText("Devamsızlık Durumu")
                self.ogrenciform.label_blok_devamsizlikbilgisi.show()
                for i,ders in enumerate(self.dersler):
                    item = QTableWidgetItem(ders)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ogrenciform.tableWidget_devamsizlikbilgisi.setItem(i, 0, item)
        if item.text() == "Şifre Değiştir":
            if self.ogrenciform.groupBox_anamenu.isVisible():
                self.ogrenciform.groupBox_anamenu.hide()
            if self.ogrenciform.groupBox_derskayit.isVisible():
                self.ogrenciform.groupBox_derskayit.hide()
            if self.ogrenciform.groupBox_NotListesi.isVisible():
                self.ogrenciform.groupBox_NotListesi.hide()
            if self.ogrenciform.groupBox_Devamsizlikdurumu.isVisible():
                self.ogrenciform.groupBox_Devamsizlikdurumu.hide()
            if self.ogrenciform.groupBox_AkademikTakvim.isVisible():
                self.ogrenciform.groupBox_AkademikTakvim.hide()
            self.ogrenciform.groupBox_sifredegistir.show()
        if item.text() == "Çıkış Yap":
            sys.exit()
    
    def Ders1(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(0,0).text()
        self.ogrenciform.pushButton_1.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_1.setIcon(QIcon(iconpath))  
        self.ogrenciform.pushButton_1.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders2(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(1,0).text()
        self.ogrenciform.pushButton_2.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_2.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_2.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders3(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(2,0).text()
        self.ogrenciform.pushButton_3.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_3.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_3.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders4(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(3,0).text()
        self.ogrenciform.pushButton_4.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_4.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_4.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders5(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(4,0).text()
        self.ogrenciform.pushButton_5.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_5.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_5.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders6(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(5,0).text()
        self.ogrenciform.pushButton_6.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_6.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_6.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders7(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(6,0).text()
        self.ogrenciform.pushButton_7.setText("Eklendi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_7.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_7.setEnabled(False)
        self.DersSec(ders)
        self.kesinlestir_check()
    def Ders8(self):
        self.ders_sayaci += 1
        ders = self.ogrenciform.tableWidget_kayit.item(7,0).text()
        self.DersSec(ders)
        self.ogrenciform.pushButton_8.setText("Eklendi")
        iconpath =  r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.pushButton_8.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_8.setEnabled(False)
        self.kesinlestir_check()
    def DersSec(self,ders):
        if ders not in self.dersler:
            self.dersler.append(ders)

    def AgnoHesapla(self):
        toplamNotKredi = 0
        toplamKredi = 0
        girilmis_ders_sayisi = 0
        for i in range(len(self.dersler1)):
            ort = 0  
            kredi = 0
            cell_ort = self.ogrenciform.tableWidget_notlarim.item(i, 5)
            if cell_ort is not None and cell_ort.text().strip() and cell_ort.text() != "Girilmedi":
                ort = float(cell_ort.text())
                girilmis_ders_sayisi += 1
            cell_kredi = self.ogrenciform.tableWidget_kayit.item(i, 2)
            if cell_kredi is not None:
                kredi = float(cell_kredi.text())
            toplamNotKredi += ort * kredi
            toplamKredi += kredi
        if girilmis_ders_sayisi == 0 or girilmis_ders_sayisi < len(self.dersler):
            return "Sonuçlandırılmadı"  
        if toplamKredi == 0:
            return "Sonuçlandırılmadı" 
        agno = toplamNotKredi / toplamKredi
        agno = round(agno, 2)
        return agno


    def kesinlestir(self):
        ogrenci_no = self.ogr_no
        ogrenci_sql.KesinlestirSet(ogrenci_no, 0)
        self.NotlarıGosterKesin()
        self.ogrenciform.pushButton_kesinlestir.setText("Kesinleştirildi")
        iconpath = r'C:\Users\Helios\Desktop\Öğrenci Bilgi Sistemi\secildi.ico'
        self.ogrenciform.label_ogrencikesinlestirme.setText("Öğrenci Kesinleştirme Durumu : Kesinleştirildi")
        self.ogrenciform.pushButton_kesinlestir.setIcon(QIcon(iconpath))
        self.ogrenciform.pushButton_kesinlestir.setEnabled(False)

    def kesinlestir_check(self):
        if self.ders_sayaci == 8 and kesinMi == True : 
            self.ogrenciform.pushButton_kesinlestir.setEnabled(True)
            self.ogrenciform.pushButton_kesinlestir.setStyleSheet(
                '''
                QPushButton {
                    border: 2px solid #a9a9a9;
                    border-radius: 15px;
                    background-color: #add8e6; /* Açık mavi tonu */
                }

                QPushButton:hover {
                    background-color: #f0f0f0; /* Biraz daha koyu mavi tonu */
                }
                '''
            )