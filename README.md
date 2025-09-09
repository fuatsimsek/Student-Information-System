# Student Information System

**A modern desktop application for managing student records, announcements, and academic processes.**  
Developed using Python and PyQt5 with SQL Server as the database backend.

---

## 📌 Overview

The **Student Information System** simplifies the management of student data and academic activities.  
It provides features such as adding, updating, deleting student records, and sending announcements via email.

---

## ✨ Features

- **Student Management:** Add, update, or delete student records easily.
- **SQL Server Integration:** Connect to an SQL Server database for data management.
- **PyQt5 Interface:** A user-friendly, modern, and clean graphical interface.
- **Teacher Announcements:** Teachers can send announcements to all registered students.
- **Email Notifications:** Notify students directly through their registered email addresses.

---

## 🛠️ Technologies Used

- **Python 3.x** — Core programming language
- **PyQt5** — GUI (Graphical User Interface)
- **SQL Server** — Database management
- **pypyodbc** — SQL Server connectivity

---

## 🚀 Getting Started

Follow these steps to set up and run the project.

### 1. Requirements
- Python 3.x  
- PyQt5  
- pypyodbc (for SQL Server connection)  
- SQL Server Management Studio (SSMS)  
- SQL Server installed on your machine

---

### 2. SQL Server Setup
1. Download and install SQL Server from Microsoft's official website.  
2. During installation, also install **SQL Server Management Studio (SSMS)**.  
3. Launch SSMS to manage your database.

---

### 3. Restoring the Database Backup
The project includes a `.bak` file named `OgrenciBilgiSistemi.bak` for database restoration.

Steps to restore:
1. Open **SSMS**.  
2. Right-click on the **Databases** section and select **Restore Database**.  
3. Choose the `.bak` file and complete the restoration process.

---

### 4. Configuring the Database Connection
Open the `baglanti_sql.py` file and update the database connection settings:

```python
Driver_Name = 'SQL SERVER'
Server_Name = 'localhost\\SQLEXPRESS'  # Replace with your server name
Database_Name = 'OgrenciBilgiSistemi'  # Database name
