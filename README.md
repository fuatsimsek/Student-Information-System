Öğrenci Bilgi Sistemi
Bu proje, Python ve PyQt5 kullanarak geliştirilen bir Öğrenci Bilgi Sistemi uygulamasıdır. Uygulama, SQL Server veritabanına bağlanarak öğrenci verilerini yönetmeye yönelik temel işlemleri sağlar.

Özellikler
Öğrenci bilgilerini ekleme, güncelleme ve silme.
SQL Server veritabanı ile bağlantı kurma ve veri yönetimi.
PyQt5 ile kullanıcı dostu bir arayüz.
Teknolojiler
Python 3.x
PyQt5
SQL Server
pypyodbc
Başlangıç
Projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

Gereksinimler
Python 3.x
PyQt5
pypyodbc (SQL Server bağlantısı için)
SQL Server Management Studio (SSMS)
SQL Server Kurulumu
İlk olarak SQL Server'i indirip kurmanız gerekecek. Microsoft'un resmi web sitesinden SQL Server'in en son sürümünü indirebilirsiniz. Kurulum sihirbazını takip ederek SQL Server'ı bilgisayarınıza kurun. Kurulum sırasında isteğe bağlı olarak SQL Server Management Studio (SSMS) de kurabilirsiniz.

SQL Server Management Studio (SSMS) Kurulumu
SQL Server kurulumu sırasında SSMS kurmadıysanız, ayrıca SSMS'yi indirip kurmanız gerekecek. Yine Microsoft'un web sitesinden SSMS'yi indirebilirsiniz.

Veritabanı Yedek Dosyasını Yükleme
Projenizdeki ".bak" uzantılı OgrenciBilgiSistemi.bak veritabanı yedek dosyasını SQL Server Management Studio kullanarak veritabanınıza geri yükleyin. SSMS'yi açın, ardından "Databases" sekmesine sağ tıklayın ve "Restore Database" seçeneğini seçin. Bu adımda ".bak" dosyasını seçip geri yükleme işlemini tamamlayın.

Bağlantı Bilgilerini Ayarlama
Projenizin içindeki baglanti_sql.py dosyasını açın ve içindeki server adını projenizin gereksinimlerine uygun olarak değiştirin. Örneğin:

Driver_Name = 'SQL SERVER'
Server_Name = 'localhost\\SQLEXPRESS'  # Sunucu adı
Database_Name = 'OgrenciBilgiSistemi'  # Veritabanı adı
Config.json Dosyasının Ayarları
Projede kayıtlı öğrencilere e-posta adresi gereklidir. Bu nedenle, proje çalıştırılmadan önce Config.json adlı dosyanın içerisine bir hotmail e-posta adresi ve şifresi girmeniz gerekmektedir.

Projeyi Başlatma
Projeyi çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

Bağlantı Testi
Veritabanına başarıyla bağlanıp bağlanmadığınızı test etmek için aşağıdaki kodu kullanabilirsiniz:

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
