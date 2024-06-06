import baglanti_sql as bag
cursor = bag.conn.cursor()
#Öğretmen giriş fonksiyonları
def BilgiKontrolOgrt(ogrtId,ogrtSifre):
    query = f"SELECT ogretmen_ad FROM dbo.ogretmen WHERE ogretmen_id = '{ogrtId}' AND ogretmen_sifre = '{ogrtSifre}'"
    cursor.execute(query)
    bilgi = cursor.fetchone()
    return bilgi[0] if bilgi else None

def GirisYapOgrt(id,sifre):
    ogrAd = BilgiKontrolOgrt(id, sifre)
    if ogrAd:
        return True
    else:
        return False

#Öğrenci devamsızlık  giriş fonksiyonları
def OgrenciDevamsizlik(ogrNo, dersKodu, ogrDevamsizlik):
    cursor = bag.conn.cursor() 
    kontrol_query = f"SELECT COUNT(*) FROM dbo.devamsizlik WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
    cursor.execute(kontrol_query)
    var_mi = cursor.fetchone()[0]
    if var_mi > 0:
        query = f"UPDATE dbo.devamsizlik SET devamsizlik_sayisi = '{ogrDevamsizlik}' WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
        cursor.execute(query)
        bag.conn.commit()
        print("Devamsızlık güncellendi")
    else:
        query = f"INSERT INTO dbo.devamsizlik (ogrenci_no, ders_kodu, devamsizlik_sayisi) VALUES ('{ogrNo}', '{dersKodu}', {ogrDevamsizlik})"
        cursor.execute(query)
        bag.conn.commit()
        print("Devamsızlık girişi yapıldı")

#Öğretmen not giriş fonksiyonları
def NotGir(ogrNo, dersKodu, vizeNotu, finalNotu):
    cursor = bag.conn.cursor()  
    kontrol_query = f"SELECT COUNT(*) FROM dbo.notlar WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
    cursor.execute(kontrol_query)
    var_mi = cursor.fetchone()[0]
    if var_mi > 0:
        update_query = f"UPDATE dbo.notlar SET vize_notu = {vizeNotu}, final_notu = {finalNotu} WHERE ogrenci_no = '{ogrNo}' AND ders_kodu = '{dersKodu}'"
        cursor.execute(update_query)
        bag.conn.commit()
        print("Notlar başarıyla güncellendi")
    else:
        query = f"INSERT INTO dbo.notlar (ogrenci_no, ders_kodu, vize_notu, final_notu) VALUES ('{ogrNo}', '{dersKodu}', {vizeNotu}, {finalNotu})"
        cursor.execute(query)
        bag.conn.commit()
        print("Notlar başarıyla kaydedildi")

#Akademisyen şifre değiştir fonksiyonları
def SifreAyniMi(OgrtNo, Sifre):
    query = f"SELECT ogretmen_sifre FROM dbo.ogretmen WHERE ogretmen_id = '{OgrtNo}'"
    cursor.execute(query)
    sifre = cursor.fetchone()
    if sifre and Sifre == sifre[0]:  
        return True
    else:
        return False

def SifreDegistir(OgrtNo, EskiSifre, YeniSifre):
    if SifreAyniMi(OgrtNo, EskiSifre ):
        query = f"UPDATE dbo.ogretmen SET ogretmen_sifre = '{YeniSifre}' WHERE ogretmen_id = '{OgrtNo}'"
        cursor.execute(query)
        cursor.commit()
        print("Şifre Güncellendi")
    else:
        print("Eski şifre yanlış")

#Öğretmen bilgilerinin Gösterme fonksiyonları
def OgrtAdGet(OgrtNo):
    query = f"SELECT ogretmen_ad FROM dbo.ogretmen WHERE ogretmen_id ='{OgrtNo}'"
    cursor.execute(query)
    ad = cursor.fetchone()
    return ad

def OgrtMailGet(OgrtNo):
    query = f"SELECT ogretmen_mail FROM dbo.ogretmen WHERE ogretmen_id ='{OgrtNo}'"
    cursor.execute(query)
    mail = cursor.fetchone()
    return mail

def OgrAdGet(OgrNoItem):
    OgrNo = OgrNoItem.text()
    query = f"SELECT ogrenci_ad, ogrenci_soyad FROM dbo.ogrenci WHERE ogrenci_no = '{OgrNo}'"
    cursor.execute(query)
    ad = cursor.fetchone() 
    if ad:
        tam_ad = f"{ad[0]} {ad[1]}"  
        return tam_ad
    else:
        return ""

def OgrMailGet():
    query = "SELECT ogrenci_mail FROM dbo.ogrenci"
    cursor.execute(query)
    mails = cursor.fetchall()[1:]
    return [mail[0] for mail in mails]

def OgrCount():
        query = "SELECT COUNT(ogrenci_no) FROM dbo.ogrenci"
        cursor.execute(query)
        result = cursor.fetchone()
        ogrenci_sayisi = result[0] if result else 0
        if ogrenci_sayisi > 0:
            ogrenci_sayisi -= 1
        return ogrenci_sayisi

def VerilenDersGet(OgrtAd):
    query = f"SELECT ders_kodu FROM dbo.dersler WHERE ders_ogretmen ='{OgrtAd}'"
    cursor.execute(query)
    dersKodu = cursor.fetchall()
    dersler = [ders[0] for ders in dersKodu]
    dersler_str = " ".join(dersler)
    return dersler_str