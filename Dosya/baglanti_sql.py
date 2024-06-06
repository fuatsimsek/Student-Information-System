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