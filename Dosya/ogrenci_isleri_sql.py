import baglanti_sql as bag
cursor = bag.conn.cursor()
#Öğrenci ekle sil ve güncelle fonksiyonları
def OgrenciEkle(ogrNo, ogrAd, ogrSoyad, ogrSifre, ogrMail="", ogrTel="", ogrKyt="", ogrFklt="", ogrBlm="", ogrSnf=""):
    kontrol_query = f"SELECT COUNT(*) FROM dbo.ogrenci WHERE ogrenci_no = '{ogrNo}'"
    cursor.execute(kontrol_query)
    var_mi = cursor.fetchone()[0]
    if var_mi > 0:
        print("Bu numaraya sahip bir öğrenci zaten var")
    else:
        query_ogrenci = f"INSERT INTO dbo.ogrenci (ogrenci_no, ogrenci_ad, ogrenci_soyad, ogrenci_sifre, ogrenci_mail, ogrenci_telefon, ogrenci_kayit_tarih, ogrenci_fakulte, ogrenci_bolum, ogrenci_sinif)  VALUES ('{ogrNo}', '{ogrAd}', '{ogrSoyad}', '{ogrSifre}', '{ogrMail}', '{ogrTel}', '{ogrKyt}','{ogrFklt}','{ogrBlm}','{ogrSnf}')"
        query_notlar = f"INSERT INTO dbo.notlar (ogrenci_no) VALUES ('{ogrNo}')"
        query_devamsizlik = f"INSERT INTO dbo.devamsizlik (ogrenci_no) VALUES ('{ogrNo}')"
        cursor.execute(query_ogrenci)
        cursor.execute(query_notlar)
        cursor.execute(query_devamsizlik)
        bag.conn.commit()
        print("Öğrenci başarıyla eklendi")

def OgrencileriGetir():
    query = "SELECT  ogrenci_ad, ogrenci_soyad, ogrenci_no, ogrenci_sifre, ogrenci_telefon, ogrenci_mail, ogrenci_fakulte, ogrenci_bolum, ogrenci_sinif FROM dbo.ogrenci"
    cursor.execute(query)
    ogrenciler = cursor.fetchall()
    return ogrenciler

def OgrenciSil(ogrNo):
    query_notlar_sil = "DELETE FROM dbo.notlar WHERE ogrenci_no = ?"
    cursor.execute(query_notlar_sil, (ogrNo,))
    bag.conn.commit()
    query_devamsizlik_sil = "DELETE FROM dbo.devamsizlik WHERE ogrenci_no = ?"
    cursor.execute(query_devamsizlik_sil, (ogrNo,))
    bag.conn.commit()
    query_ogrenci_sil = "DELETE FROM dbo.ogrenci WHERE ogrenci_no = ?"
    cursor.execute(query_ogrenci_sil, (ogrNo,))
    bag.conn.commit()
    print("Öğrenci başarıyla silindi")

def OgrenciGuncelle(ogrNo, yeniAd, yeniSifre, yeniMail, yeniTel, yeniAdr):
    query = f"UPDATE dbo.ogrenci SET ogrenci_ad = '{yeniAd}', ogrenci_sifre = '{yeniSifre}', ogrenci_mail = '{yeniMail}', ogrenci_telefon = '{yeniTel}', ogrenci_adress = '{yeniAdr}' WHERE ogrenci_no = '{ogrNo}'"
    cursor.execute(query)
    bag.conn.commit()
    print("Öğrenci başarıyla güncellendi")