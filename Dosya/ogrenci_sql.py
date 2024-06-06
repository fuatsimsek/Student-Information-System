import baglanti_sql as bag
from datetime import datetime

cursor = bag.conn.cursor()
#Öğrenci giriş fonksiyonları
def BilgiKontrolOgr(ogrNo, ogrSifre):
    query = f"SELECT ogrenci_ad FROM dbo.ogrenci WHERE ogrenci_no = '{ogrNo}' AND ogrenci_sifre = '{ogrSifre}'"
    cursor.execute(query)
    bilgi = cursor.fetchone()
    return bilgi[0] if bilgi else None

def GirisYapOgr(ogrenci_no, ogrenci_sifre):
    ogrAd = BilgiKontrolOgr(ogrenci_no, ogrenci_sifre)
    if ogrAd:
        return True
    else:
        return False

#Öğrenci not getirme fonksiyonları
def NotGetir(ogrNo, dersKodu):
    # Öğrencinin notlarını sorgula
    query = f"SELECT vize_notu, final_notu FROM dbo.notlar WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
    cursor.execute(query)
    notlar = cursor.fetchone()
    if notlar:
        vize_notu, final_notu = notlar
        return vize_notu, final_notu
    else:
        print("Bu öğrenci ve ders için not bulunamadı")
        return "Girilmedi", "Girilmedi"

#Öğrenci devamsızlık getirme fonksiyonları
def DevamsizlikGoster(ogrNo, dersKodu):
    query = f"SELECT devamsizlik_sayisi FROM dbo.devamsizlik WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
    cursor.execute(query)
    devamsizlik = cursor.fetchone()
    
    if devamsizlik:
        devamsiz = devamsizlik[0]
        print("Devamsızlık:", devamsiz, dersKodu)
    else:
        print("Numara kayıtlı değil ")

def DevamsizlikGetir(OgrNo):
    query = f"SELECT ders_kodu, devamsizlik_sayisi FROM dbo.devamsizlik WHERE ogrenci_no = '{OgrNo}'"
    cursor.execute(query)
    dersler = cursor.fetchall()[1:]
    return dersler

#Dersleri yazdırma fonksiyonları
def DersGetir():
    query = "SELECT ders_kodu, ders_adi, ders_kredi, ders_sinif, ders_alis FROM dbo.dersler"
    cursor.execute(query)
    dersler = cursor.fetchall()[1:]
    return dersler

#Şifre değiştirme fonksiyonları
def SifreAyniMi(OgrNo, Sifre):
    query = f"SELECT ogrenci_sifre FROM dbo.ogrenci WHERE ogrenci_no = '{OgrNo}'"
    cursor.execute(query)
    sifre = cursor.fetchone()
    if sifre and Sifre == sifre[0]:
        return True
    else:
        return False

def SifreDegistir(OgrNo, EskiSifre, YeniSifre):
    if SifreAyniMi(OgrNo, EskiSifre):
        query = f"UPDATE dbo.ogrenci SET ogrenci_sifre = '{YeniSifre}' WHERE ogrenci_no = '{OgrNo}'"
        cursor.execute(query)
        cursor.commit()
        print("Şifre Güncellendi")
    else:
        print("Eski şifre yanlış")

#Öğrenci bilgilerinin Gösterme fonksiyonları
def OgrAdGet(OgrNo):
    query = f"SELECT ogrenci_ad FROM dbo.ogrenci WHERE ogrenci_no ='{OgrNo}'"
    cursor.execute(query)
    ad = cursor.fetchone()
    return ad

def OgrSoyadGet(OgrNo):
    query = f"SELECT ogrenci_soyad FROM dbo.ogrenci WHERE ogrenci_no ='{OgrNo}'"
    cursor.execute(query)
    soyad = cursor.fetchone()
    return soyad

def OgrMailGet(OgrNo):
    query = f"SELECT ogrenci_mail FROM dbo.ogrenci WHERE ogrenci_no ='{OgrNo}'"
    cursor.execute(query)
    mail = cursor.fetchone()
    return mail

def OgrFakulteGet(OgrNo):
    query = f"SELECT ogrenci_fakulte FROM dbo.ogrenci WHERE ogrenci_no ='{OgrNo}'"
    cursor.execute(query)
    fakulte = cursor.fetchone()
    return fakulte

def OgrKayitGet(OgrNo):
    query = f"SELECT ogrenci_kayit_tarih FROM dbo.ogrenci WHERE ogrenci_no ='{OgrNo}'"
    cursor.execute(query)
    kayit = cursor.fetchone()
    return kayit[0].strftime("%d.%m.%Y")

def KesinlestirGet(OgrNo):
    query = f"SELECT ogrenci_kesin FROM dbo.ogrenci WHERE ogrenci_no = ?"
    cursor.execute(query, (OgrNo,))
    kesin = cursor.fetchone()
    if kesin is not None and kesin[0] == 0:
        return False
    else:
        return True
#print(KesinlestirGet(222201346))
def KesinlestirSet(OgrNo, kesinMi):
    query = f"UPDATE dbo.ogrenci SET ogrenci_kesin = '{kesinMi}' WHERE ogrenci_no = '{OgrNo}'"
    cursor.execute(query)
    cursor.commit()
#KesinlestirSet(222201346, 1)