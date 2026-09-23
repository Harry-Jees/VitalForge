# Vital Forge — Build & Setup Guide

Vital Forge is a Python Tkinter fitness-tracking application using MySQL for real user accounts and Matplotlib for progress charts.

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