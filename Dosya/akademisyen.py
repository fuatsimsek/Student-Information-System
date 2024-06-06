from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from akademisyen_python import Ui_Form_akademisyen
from PyQt5.QtGui import QColor, QFont,QIcon
from PyQt5.QtCore import QTimer
import sys
import email_sender
import ogretmen_sql


class akademisyenPage(QWidget):
    def __init__(self, ogrt_no) -> None:
        super().__init__()
        self.ogrt_no = ogrt_no
        ogrt_ad = str(ogretmen_sql.OgrtAdGet(self.ogrt_no)[0])
        ogrt_mail = str(ogretmen_sql.OgrtMailGet(self.ogrt_no)[0])
        self.akademisyenform = Ui_Form_akademisyen()
        self.akademisyenform.setupUi(self)
        self.akademisyenform.groupBox_devamsizlik.hide()
        self.akademisyenform.groupBox_notgirisi.hide()
        self.akademisyenform.groupBox_sifredegistir.hide()
        self.akademisyenform.groupBox_duyuruyap.hide()
        self.akademisyenform.groupBox_anamenu.show()    
        self.sifre = "1"
        self.eskisifre_clicked = False
        self.yenisifre1_clicked = False
        self.yenisifre2_clicked = False
        self.baslik_clicked = False
        self.metin_clicked = False
        self.style = """
            QLabel {
                font-weight: bold;
                border: none; /* Çerçeveyi kaldırmak için */
                color: maroon;
                font-size: 16px; /* Font boyutunu artırmak için */
            }
        """
        self.style2 = """
            QLabel {
                font-weight: bold;
                border: none; /* Çerçeveyi kaldırmak için */
                color: darkgreen;
                font-size: 16px; /* Font boyutunu artırmak için */
            }
        """

        self.akademisyenform.tableWidget_notgir_profilbilgileri.hide()
        self.akademisyenform.label_blok_profilbilgileri.hide()
        self.akademisyenform.tableWidget_devamsizlikgirprofil.hide()
        self.akademisyenform.label_blok_devamsizlikprofil.hide()
       
        self.akademisyenform.pushButton_devamsizlikonayla.setEnabled(False)
        self.akademisyenform.tableWidget_devamsizlik.itemChanged.connect(self.girislerikontrolEt)
        self.akademisyenform.pushButton_devamsizlikonayla.clicked.connect(self.devamsizlikGonder)
        self.akademisyenform.tableWidget_devamsizlik.itemChanged.connect(self.girislerikontrolEt4)

        self.akademisyenform.pushButton_notsonuclandir.setEnabled(False)
        self.akademisyenform.tableWidget_notgir.itemChanged.connect(self.girislerikontrolEt2)
        self.akademisyenform.pushButton_notsonuclandir.clicked.connect(self.notsonuclandirgonder)
        self.akademisyenform.tableWidget_notgir.itemChanged.connect(self.girislerikontrolEt3)
        
        self.akademisyenform.pushButton_gonder.clicked.connect(self.duyuruGonder)

        self.akademisyenform.tableWidget_devamsizlik.item

        font2 = QFont("Microsoft YaHei UI Light")
        
        font2.setPointSize(25)
        self.akademisyenform.lineEdit_eskisifre.setFont(font2)

        font2.setPointSize(25)
        self.akademisyenform.lineEdit_yenisifre1.setFont(font2)

        font2.setPointSize(25)
        self.akademisyenform.lineEdit_yenisifre2.setFont(font2)
        self.akademisyenform.lineEdit_eskisifre.setEchoMode(QLineEdit.Normal)
        self.akademisyenform.lineEdit_yenisifre1.setEchoMode(QLineEdit.Normal)
        self.akademisyenform.lineEdit_yenisifre2.setEchoMode(QLineEdit.Normal)
        self.akademisyenform.lineEdit_eskisifre.setText("Mevcut şifre")
        self.akademisyenform.lineEdit_yenisifre1.setText("Yeni şifre")
        self.akademisyenform.lineEdit_yenisifre2.setText("Yeni şifreyi tekrar yaz")       
        self.akademisyenform.lineEdit_baslik.setText("Başlık bölümü")
        self.akademisyenform.textEdit_metin.setPlainText("Metin bölümü")      
        self.akademisyenform.lineEdit_eskisifre.mousePressEvent = self.selected_eskisifre
        self.akademisyenform.lineEdit_yenisifre1.mousePressEvent = self.selected_yenisifre1
        self.akademisyenform.lineEdit_yenisifre2.mousePressEvent = self.selected_yenisifre2
        self.akademisyenform.pushButton_sifredegistir.clicked.connect(self.sifreDegistir)
        self.akademisyenform.lineEdit_baslik.mousePressEvent = self.selected_baslik
        self.akademisyenform.textEdit_metin.mousePressEvent = self.selected_metin
        self.akademisyenform.pushButton_ogrtisimsoyisim.setText(ogrt_ad)
        self.akademisyenform.pushButton_ogrtakademisyennumara.setText("Akademisyen Numarası:"+str(self.ogrt_no))  
        self.akademisyenform.pushButton_ogrtemail.setText(ogrt_mail) 
        self.akademisyenform.pushButton_dersgorenogrenc.setText("Aktif Dönemde Ders Gören Öğrenciler \n" + str(ogretmen_sql.OgrCount()))
        self.akademisyenform.pushButton_verilendersler.setText("Aktif Dönemde Verilen Dersler \n" + str(ogretmen_sql.VerilenDersGet(ogrt_ad)))
        self.akademisyenform.listWidget_menu.itemClicked.connect(self.item_clicked)
        self.akademisyenform.lineEdit_eskisifre.setFocusPolicy(Qt.ClickFocus)
        self.akademisyenform.lineEdit_yenisifre1.setFocusPolicy(Qt.ClickFocus)
        self.akademisyenform.lineEdit_yenisifre2.setFocusPolicy(Qt.ClickFocus)
    def girislerikontrolEt(self):
        tablo = self.akademisyenform.tableWidget_devamsizlik
        rowCount = tablo.rowCount()
        columnCount = tablo.columnCount()
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row,col)
                if item is None or item.text() == "":
                    self.akademisyenform.pushButton_devamsizlikonayla.setEnabled(False)
                    return
        self.akademisyenform.pushButton_devamsizlikonayla.setEnabled(True)

    def girislerikontrolEt2(self):
        tablo = self.akademisyenform.tableWidget_notgir
        rowCount = tablo.rowCount()
        columnCount = tablo.columnCount()
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row,col)
                if item is None or item.text() == "":
                    self.akademisyenform.pushButton_notsonuclandir.setEnabled(False)
                    return
        self.akademisyenform.pushButton_notsonuclandir.setEnabled(True)

    def girislerikontrolEt3(self):
        tablo = self.akademisyenform.tableWidget_notgir
        rowCount = tablo.rowCount()
        columnCount = tablo.columnCount()-3
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row,col)
                if item is None or item.text() == "":
                    self.akademisyenform.tableWidget_notgir_profilbilgileri.hide()
                    self.akademisyenform.label_blok_profilbilgileri.hide()
                    self.akademisyenform.label_engelnotgirisi.hide()
                    self.akademisyenform.label_engelnotgirisi2.hide()
                    self.akademisyenform.label_engelnotgirisi3.hide()
                    return
        self.akademisyenform.tableWidget_notgir_profilbilgileri.show()
        self.akademisyenform.label_blok_profilbilgileri.show()
        self.akademisyenform.label_engelnotgirisi.show()
        self.akademisyenform.label_engelnotgirisi2.show()
        self.akademisyenform.label_engelnotgirisi3.show()
        
        hedef_item = self.akademisyenform.tableWidget_notgir_profilbilgileri.item(0, 0)
        hedef_item2 = self.akademisyenform.tableWidget_notgir_profilbilgileri.item(0, 1)
        kaynak_item = self.akademisyenform.tableWidget_notgir.item(0, 0)
        kaynak_item2 = ogretmen_sql.OgrAdGet(kaynak_item)

        if hedef_item is not None and kaynak_item is not None:
            hedef_item.setText(kaynak_item.text())
            hedef_item2.setText(kaynak_item2)

    def girislerikontrolEt4(self):
        tablo = self.akademisyenform.tableWidget_devamsizlik
        rowCount = tablo.rowCount()
        columnCount = tablo.columnCount() - 2
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row, col)
                if item is None or item.text() == "":
                    self.akademisyenform.tableWidget_devamsizlikgirprofil.hide()
                    self.akademisyenform.label_blok_devamsizlikprofil.hide()
                    self.akademisyenform.label_engeldevamsizlilk.hide()
                    self.akademisyenform.label_engeldevamsizlilk2.hide()
                    self.akademisyenform.label_engeldevamsizlilk3.hide()
                    return
        self.akademisyenform.tableWidget_devamsizlikgirprofil.show()
        self.akademisyenform.label_blok_devamsizlikprofil.show()    
        self.akademisyenform.label_engeldevamsizlilk.show()
        self.akademisyenform.label_engeldevamsizlilk2.show()
        self.akademisyenform.label_engeldevamsizlilk3.show()
        hedef_item = self.akademisyenform.tableWidget_devamsizlikgirprofil.item(0, 0)
        hedef_item2 = self.akademisyenform.tableWidget_devamsizlikgirprofil.item(0, 1)
        kaynak_item = self.akademisyenform.tableWidget_devamsizlik.item(0, 0)
        kaynak_item2 = ogretmen_sql.OgrAdGet(kaynak_item)

        if hedef_item is not None and kaynak_item is not None:
            hedef_item.setText(kaynak_item.text())
            hedef_item2.setText(kaynak_item2)

    def duyuruGonder(self):
        ogrMailList = ogretmen_sql.OgrMailGet()
        if self.akademisyenform.lineEdit_baslik.text() != "" and self.akademisyenform.textEdit_metin.toPlainText() != "":
            baslik = self.akademisyenform.lineEdit_baslik.text()
            govde = self.akademisyenform.textEdit_metin.toPlainText()
            email_sender.sender(baslik, govde, email_sender.sender_mail, ogrMailList, email_sender.sender_pwd)    
            self.akademisyenform.label_bilgi.setStyleSheet(self.style2)
            self.akademisyenform.label_bilgi.setText("Duyuru başarıyla öğrencilere gönderildi.")
            QTimer.singleShot(3000, self.clearText3)
        elif self.akademisyenform.lineEdit_baslik.text() == "" and self.akademisyenform.textEdit_metin.toPlainText() != "":
            self.akademisyenform.label_bilgi.setText("Başlık bölümü boş bırakılamaz.")
            self.akademisyenform.label_bilgi.setStyleSheet(self.style)
            QTimer.singleShot(3000, self.clearText3)
        elif self.akademisyenform.lineEdit_baslik.text() != "" and self.akademisyenform.textEdit_metin.toPlainText() == "":
            self.akademisyenform.label_bilgi.setText("Metin bölümü boş bırakılamaz.")
            self.akademisyenform.label_bilgi.setStyleSheet(self.style)
            QTimer.singleShot(3000, self.clearText3)
        else:
            self.akademisyenform.label_bilgi.setText("Başlık ve metin bölümü boş bırakılamaz.")
            self.akademisyenform.label_bilgi.setStyleSheet(self.style)
            QTimer.singleShot(3000, self.clearText3)
     
    def devamsizlikGonder(self):
        tablo = self.akademisyenform.tableWidget_devamsizlik
        rowCount = tablo.rowCount()
        for row in range(rowCount):
            ogrNo = tablo.item(row, 0).text()  
            ogrDevamsizlik = tablo.item(row, 2).text()  
            dersKodu = tablo.item(row,1).text() 
            ogretmen_sql.OgrenciDevamsizlik(ogrNo, dersKodu, ogrDevamsizlik)  
            tablo.setItem(row, 1, QTableWidgetItem("")) 

    def notsonuclandirgonder(self):
        tablo = self.akademisyenform.tableWidget_notgir
        rowCount = tablo.rowCount()
        columnCount = tablo.columnCount()
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row, col)
                if item is not None:
                    vizeNotu = tablo.item(row, 2).text()  
                    finalNotu = tablo.item(row, 3).text()  
                    ogrNo = tablo.item(row, 0).text()  
                    dersKodu = tablo.item(row, 1).text()  
            ogretmen_sql.NotGir(int(ogrNo), dersKodu, float(vizeNotu), float(finalNotu))
        for row in range(rowCount):
            for col in range(columnCount):
                item = tablo.item(row, col)
                if item is not None:
                     item.setText("")

    def selected_eskisifre(self, event):
        if not self.eskisifre_clicked:
            font3 = QFont()
            font3.bold()
            self.akademisyenform.lineEdit_eskisifre.setFont(font3)
            self.akademisyenform.lineEdit_eskisifre.setText("")
            self.akademisyenform.lineEdit_eskisifre.setEchoMode(QLineEdit.Password)
            self.eskisifre_clicked = True
        
    def selected_yenisifre1(self, event):
        if not self.yenisifre1_clicked:
            font4 = QFont()
            font4.bold()
            self.akademisyenform.lineEdit_eskisifre.setFont(font4)
            self.akademisyenform.lineEdit_yenisifre1.setText("")
            self.akademisyenform.lineEdit_yenisifre1.setEchoMode(QLineEdit.Password)
            self.yenisifre1_clicked = True
            
    def selected_yenisifre2(self, event):
        if not self.yenisifre2_clicked:
            font5 = QFont()
            font5.bold()
            self.akademisyenform.lineEdit_eskisifre.setFont(font5)
            self.akademisyenform.lineEdit_yenisifre2.setText("")
            self.akademisyenform.lineEdit_yenisifre2.setEchoMode(QLineEdit.Password)
            self.yenisifre2_clicked = True

    def selected_baslik(self, event):
        if not self.baslik_clicked:
            self.akademisyenform.lineEdit_baslik.setText("")
            self.baslik_clicked = True

    def selected_metin(self, event):
        if not self.metin_clicked:
            self.akademisyenform.textEdit_metin.setText("")
            self.metin_clicked = True
    
    def sifreDegistir(self):
        akademisyen_id = 1
        yeni_sifre = self.akademisyenform.lineEdit_yenisifre1.text()
        yeni_sifre_tekrar = self.akademisyenform.lineEdit_yenisifre2.text()
        eski_sifre = self.akademisyenform.lineEdit_eskisifre.text()
        if yeni_sifre == yeni_sifre_tekrar:
            if ogretmen_sql.SifreAyniMi(akademisyen_id, eski_sifre): 
                if self.akademisyenform.checkBox_girisekraninadon.isChecked():
                    ogretmen_sql.SifreDegistir(akademisyen_id, eski_sifre, yeni_sifre)
                    self.akademisyenform.label_sifreguncellendi.setStyleSheet("QLabel { color: #008000; font-size: 16px; font-weight: bold; }")
                    self.akademisyenform.label_sifreguncellendi.setText("Şifreniz başarıyla güncellendi.")
                    QTimer.singleShot(3000,self.clearText2)
                else:
                    ogretmen_sql.SifreDegistir(akademisyen_id, eski_sifre, yeni_sifre)
                    self.akademisyenform.label_sifreguncellendi.setStyleSheet("QLabel { color: #008000; font-size: 16px; font-weight: bold; }")
                    self.akademisyenform.label_sifreguncellendi.setText("Şifreniz başarıyla güncellendi.")
                    QTimer.singleShot(3000, self.clearText)
            else:
                self.akademisyenform.label_sifreguncellendi.setStyleSheet("QLabel { color: maroon; font-size: 16px; font-weight: bold; }")
                self.akademisyenform.label_sifreguncellendi.setText("Eski şifren yanlış girildi. Lütfen tekrar girin.")
                QTimer.singleShot(3000, self.clearText) 
        else:
            self.akademisyenform.label_sifreguncellendi.setStyleSheet("QLabel { color: maroon; font-size: 16px; font-weight: bold; }")
            self.akademisyenform.label_sifreguncellendi.setText("Yeni şifreler eşleşmiyor. Yeni şifreyi tekrar girin.") 
            QTimer.singleShot(3000, self.clearText)

    def clearText(self):
        self.akademisyenform.label_sifreguncellendi.setText("")

    def clearText2(self):
        sys.exit()

    def clearText3(self):
        self.akademisyenform.label_bilgi.setText("")    

    def item_clicked(self,item):
        print("Tıklanan öğe:", item.text())
        if item.text() == "Ana Menü":
            if self.akademisyenform.groupBox_devamsizlik.isVisible():
                self.akademisyenform.groupBox_devamsizlik.hide()
            if self.akademisyenform.groupBox_notgirisi.isVisible():
                self.akademisyenform.groupBox_notgirisi.hide()
            if self.akademisyenform.groupBox_sifredegistir.isVisible():
                self.akademisyenform.groupBox_sifredegistir.hide()
            if self.akademisyenform.groupBox_duyuruyap.isVisible():
                self.akademisyenform.groupBox_duyuruyap.hide()
            self.akademisyenform.groupBox_anamenu.show()
        if item.text() == "Not Girişi":
            if self.akademisyenform.groupBox_devamsizlik.isVisible():
                self.akademisyenform.groupBox_devamsizlik.hide()
            if self.akademisyenform.groupBox_anamenu.isVisible():
                self.akademisyenform.groupBox_anamenu.hide()
            if self.akademisyenform.groupBox_sifredegistir.isVisible():
                self.akademisyenform.groupBox_sifredegistir.hide()
            if self.akademisyenform.groupBox_duyuruyap.isVisible():
                self.akademisyenform.groupBox_duyuruyap.hide()
            self.akademisyenform.groupBox_notgirisi.show()
        if item.text() == "Devamsızlık Girişi":
            if self.akademisyenform.groupBox_anamenu.isVisible():
                self.akademisyenform.groupBox_anamenu.hide()
            if self.akademisyenform.groupBox_notgirisi.isVisible():
                self.akademisyenform.groupBox_notgirisi.hide()
            if self.akademisyenform.groupBox_sifredegistir.isVisible():
                self.akademisyenform.groupBox_sifredegistir.hide()
            if self.akademisyenform.groupBox_duyuruyap.isVisible():
                self.akademisyenform.groupBox_duyuruyap.hide()
            self.akademisyenform.groupBox_devamsizlik.show()
        if item.text() == "Şifre Değiştir":
            if self.akademisyenform.groupBox_devamsizlik.isVisible():
                self.akademisyenform.groupBox_devamsizlik.hide()
            if self.akademisyenform.groupBox_notgirisi.isVisible():
                self.akademisyenform.groupBox_notgirisi.hide()
            if self.akademisyenform.groupBox_anamenu.isVisible():
                self.akademisyenform.groupBox_anamenu.hide()
            if self.akademisyenform.groupBox_duyuruyap.isVisible():
                self.akademisyenform.groupBox_duyuruyap.hide()
            self.akademisyenform.groupBox_sifredegistir.show()
        if item.text() == "Duyuru Yap":
            if self.akademisyenform.groupBox_devamsizlik.isVisible():
                self.akademisyenform.groupBox_devamsizlik.hide()
            if self.akademisyenform.groupBox_notgirisi.isVisible():
                self.akademisyenform.groupBox_notgirisi.hide()
            if self.akademisyenform.groupBox_anamenu.isVisible():
                self.akademisyenform.groupBox_anamenu.hide()
            if self.akademisyenform.groupBox_sifredegistir.isVisible():
                self.akademisyenform.groupBox_sifredegistir.hide()
            self.akademisyenform.groupBox_duyuruyap.show()        
        if item.text() == "Çıkış Yap":
            sys.exit()
        