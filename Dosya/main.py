from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from obsgiris_python import Ui_Form_main
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QObject, QEvent
from ogrenci import ogrenciPage
from akademisyen import akademisyenPage
from ogrenci_isleri import ogrenci_isleriPage
import ogrenci_sql
import ogretmen_sql
class MainPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.obsgirisform = Ui_Form_main()
        self.obsgirisform.setupUi(self)      
        self.ogrenci_isleriform = ogrenci_isleriPage()
        self.obsgirisform.lineEdit_email_2.setFocusPolicy(Qt.ClickFocus)
        self.obsgirisform.lineEdit_sifre_4.setFocusPolicy(Qt.ClickFocus)
        self.email_clicked = False
        self.sifre_clicked = False
        self.obsgirisform.lineEdit_email_2.setText("Numara")
        font = QFont("Microsoft YaHei UI Light")
        font.setPointSize(25)
        self.obsgirisform.lineEdit_email_2.setFont(font)
        self.obsgirisform.lineEdit_sifre_4.setEchoMode(QLineEdit.Normal) 
        self.obsgirisform.lineEdit_sifre_4.setText("Şifre")   
        font2 = QFont("Microsoft Yahei UI Light")
        font2.setPointSize(25)
        self.obsgirisform.lineEdit_sifre_4.setFont(font2)
        font3 = QFont("Microsoft Yahei UI Light")
        font3.setPointSize(13)
        self.obsgirisform.radioButton_akademisyen_4.setFont(font3)
        self.obsgirisform.radioButton_ogrenci_4.setFont(font3)
        self.obsgirisform.radioButton_ogrenciisleri_4.setFont(font3)
        font4 = QFont("Microsoft Yahei UI Light")
        font4.setPointSize(12)
        self.obsgirisform.label_giris_2.setFont(font4)
        self.obsgirisform.label_giris_2.setStyleSheet("color: maroon;")
        self.obsgirisform.label_giris_2.colorCount
        self.obsgirisform.label_giris_2.setText("")
        self.obsgirisform.lineEdit_email_2.mousePressEvent = self.selected_email
        self.obsgirisform.lineEdit_sifre_4.mousePressEvent = self.selected_sifre
        self.obsgirisform.pushButton_giris_2.clicked.connect(self.girisKontrol)  
    
    def selected_email(self, event):
        if not self.email_clicked:
            self.obsgirisform.lineEdit_email_2.setText("")
            font5 = QFont()
            font5.bold()
            self.obsgirisform.lineEdit_email_2.setFont(font5)
            self.email_clicked = True
        
    def selected_sifre(self, event):
        if not self.sifre_clicked:
            font6 = QFont()
            font6.bold()
            self.obsgirisform.lineEdit_sifre_4.setFont(font6)
            self.obsgirisform.lineEdit_sifre_4.setText("")
            self.obsgirisform.lineEdit_sifre_4.setEchoMode(QLineEdit.Password)
            self.sifre_clicked = True
    
    def girisKontrol(self):
        if self.obsgirisform.radioButton_ogrenci_4.isChecked():   
            ogrenci_no = self.obsgirisform.lineEdit_email_2.text()
            ogrenci_sifre = self.obsgirisform.lineEdit_sifre_4.text()
            ogrAd = ogrenci_sql.GirisYapOgr(ogrenci_no, ogrenci_sifre)
            if ogrAd: 
                self.obsgirisform.label_giris_2.setText("giris yapıldı")
                self.hide()
                self.ogrenciform = ogrenciPage(ogrenci_no)
                self.ogrenciform.show()
            else:
                self.obsgirisform.label_giris_2.setText("Öğrenci numarası veya şifre yanlış.")
        elif self.obsgirisform.radioButton_akademisyen_4.isChecked():
            ogretmen_no = self.obsgirisform.lineEdit_email_2.text()
            ogretmen_sifre = self.obsgirisform.lineEdit_sifre_4.text()
            ogrtAd = ogretmen_sql.GirisYapOgrt(ogretmen_no,ogretmen_sifre)
            if ogrtAd:
                self.obsgirisform.label_giris_2.setText("giris yapıldı")
                self.hide()
                self.akademisyenform = akademisyenPage(ogretmen_no)
                self.akademisyenform.show()
            else:
                self.obsgirisform.label_giris_2.setText("Akademisyen numarası veya şifre yanlış.")
        elif self.obsgirisform.radioButton_ogrenciisleri_4.isChecked():
            if self.obsgirisform.lineEdit_email_2.text() == "5" and self.obsgirisform.lineEdit_sifre_4.text() == "6":
                self.hide()
                self.ogrenci_isleriform.show()
            else:
                self.obsgirisform.label_giris_2.setText("Öğrenci İşleri numarası veya şifre yanlış.")
        else:
            self.obsgirisform.label_giris_2.setText("Lütfen bir seçim yapın.")  
app = QApplication([])
pencere = MainPage()
pencere.show()
app.exec_()
