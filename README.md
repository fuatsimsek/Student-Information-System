**Öğrenci Bilgi Sistemi**
Bu proje, Python ve PyQt5 kullanarak geliştirilen bir Öğrenci Bilgi Sistemi uygulamasıdır. Uygulama, SQL Server veritabanına bağlanarak öğrenci verilerini yönetmeye yönelik temel işlemleri sağlar. Kullanıcılar, öğrenci bilgilerini ekleyebilir, güncelleyebilir, silebilir ve öğretmenler duyuru yapabilir.

**Özellikler**
-> Öğrenci Bilgileri Yönetimi: Öğrenci bilgilerini ekleyin, güncelleyin veya silin.
-> SQL Server Bağlantısı: SQL Server veritabanına bağlantı kurarak veri yönetimini sağlayın.
-> PyQt5 Arayüzü: Kullanıcı dostu, modern ve sade bir arayüz ile işlem yapın.
-> Öğretmen Duyuruları: Sistemde kayıtlı tüm öğrencilere öğretmenlerin duyuru yapabilmesi.
-> E-posta Entegrasyonu: Öğrencilerin e-posta adreslerini kullanarak duyuru ve bildirimleri iletin.

**Teknolojiler**
-> Python 3.x
-> PyQt5 – GUI (Grafiksel Kullanıcı Arayüzü) için
-> SQL Server – Veritabanı yönetimi için
-> pypyodbc – SQL Server bağlantısı için

_Başlangıç_
Bu projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

**Gereksinimler**
Python 3.x
PyQt5
pypyodbc (SQL Server bağlantısı için)
SQL Server Management Studio (SSMS)

SQL Server Kurulumu
İlk olarak, SQL Server'ı indirip kurmanız gerekecek. Microsoft'un resmi web sitesinden SQL Server'in en son sürümünü indirebilirsiniz. Kurulum sırasında SQL Server Management Studio (SSMS)'yi de kurmayı unutmayın.

SQL Server Management Studio (SSMS) Kurulumu
SSMS'yi indirmek için Microsoft'un web sitesini ziyaret edebilirsiniz. SSMS, veritabanınızı yönetmek için kullanacağınız araçtır.

Veritabanı Yedek Dosyasını Yükleme
Projenizdeki ".bak" uzantılı OgrenciBilgiSistemi.bak veritabanı yedek dosyasını, SQL Server Management Studio kullanarak veritabanınıza geri yükleyin:
- SSMS'yi açın.
- "Databases" sekmesine sağ tıklayın ve "Restore Database" seçeneğini seçin.
- Yedek dosyasını seçin ve işlemi tamamlayın.

Bağlantı Bilgilerini Ayarlama
Projede yer alan baglanti_sql.py dosyasını açın ve aşağıdaki bağlantı bilgilerini kendi sisteminize uygun şekilde güncelleyin:

```python
Driver_Name = 'SQL SERVER'
Server_Name = 'localhost\\SQLEXPRESS'  # Sunucu adı
Database_Name = 'OgrenciBilgiSistemi'  # Veritabanı adı
Config.json Dosyasının Ayarları Projede kayıtlı öğrencilere e-posta adresi gereklidir. Bu nedenle, proje çalıştırılmadan önce Config.json adlı dosyanın içerisine geçerli bir hotmail adresi ve şifresi girmeniz gerekmektedir.

Projeyi Başlatma Projeyi başlatmak için aşağıdaki adımları izleyebilirsiniz.

Bağlantı Testi Veritabanına başarıyla bağlanıp bağlanmadığınızı test etmek için aşağıdaki Python kodunu kullanabilirsiniz:

Python
import pypyodbc as odbc

Driver_Name = 'SQL SERVER'
Server_Name = 'localhost\\SQLEXPRESS'
Database_Name = 'OgrenciBilgiSistemi'

connection_string = f"""
DRIVER={{{Driver_Name}}};
SERVER={Server_Name};
DATABASE={Database_Name};
Trusted_Connection=yes;
"""

try:
    conn = odbc.connect(connection_string)
    print("Bağlantı başarılı")
except odbc.DatabaseError as e:
    print(str(e.value[1]))
except odbc.Error as e:
    print(str(e.value[1]))
Öğretmen Duyuru Özelliği Sistemdeki öğretmenler, öğrencilerin e-posta adreslerine duyuru gönderebilir. Bu özellik, öğretmenlerin öğrencilere önemli bilgileri iletmelerini sağlar. Duyurular, veritabanındaki kayıtlı e-posta adreslerine otomatik olarak iletilir.

Ekran Görüntüleri

Ana Menü Ekran Görüntüsü ![1](https://github.com/user-attachments/assets/e648a79c-6672-4a66-8243-a540041a52ce)

Öğrenci Menü Ekran Görüntüsü ![2](https://github.com/user-attachments/assets/27c612fb-6759-4b9e-98b0-96ca2af99f96)

Ders Kayıt Ekran Görüntüsü ![3](https://github.com/user-attachments/assets/46e5402d-ca4c-4b98-8ec4-0fcff110df06)

Öğretmen Menü Ekran Görüntüsü ![4](https://github.com/user-attachments/assets/b8447d3a-5576-4d54-bae5-6288f819b5c5)

Öğretmen Not Giriş Ekran Görüntüsü ![5](https://github.com/user-attachments/assets/42ea7a50-a9a4-452a-ab0c-56a35746153b)
