# Vital Forge — Build & Setup Guide

Vital Forge is a Python Tkinter fitness-tracking application using MySQL for real user accounts and Matplotlib for progress charts.

## MySQL Configuration

The application connects directly to the existing Aiven `defaultdb` database. Copy `.secrets.example.ini` to `.secrets.ini` and put the Aiven password in that local file:

```ini
[mysql]
password = your-rotated-aiven-password
```

`.secrets.ini` is excluded from Git. `MYSQL_HOST`, `MYSQL_PORT`, and `MYSQL_USER` can also be overridden through environment variables. Vital Forge always uses `defaultdb`. Run `python database/setup.py` to create the application tables and seed data there; setup does not create or rename databases.

---

## 1. Project Structure

```text
VitalForge/
│
├── main.py
├── config.py
├── ui_components.py
├── screens.py
├── data.py
├── utils.py
├── charts.py
├── requirements.txt
│
├── database/
│   ├── connection.py
│   ├── setup.py
│   ├── schema.sql
│   └── queries.py
│
├── assets/
│   └── logo.png
│
└── guides/
    └── BUILD.md