# 🍽️ Smart POS – Mpepo Kitchen

**Smart POS (Mpepo Kitchen)** is a full-stack point-of-sale system built with **FastAPI (Python)** and **Flutter (Dart)**, designed for restaurant operations and compliant with **ZRA-style Smart Invoicing** standards.

---

## 📋 Project Overview

Smart POS streamlines the daily operations of a restaurant by allowing staff to:
- Add and manage food and beverage items.
- Process customer orders quickly.
- Generate **ZRA-compliant tax invoices** automatically.
- Continue processing sales **offline** — queued until network is restored.

The project is branded for **Mpepo Kitchen**, a fictional restaurant used as the business case study.

---

## 🏗️ System Components

### **Backend (FastAPI)**
- Handles all business logic, database storage, and invoice generation.
- Integrates with a **mock ZRA tax API** for testing invoice submission.
- Uses **SQLite** for lightweight local storage.

### **Frontend (Flutter Mobile App)**
- User-friendly POS interface for Android devices.
- Displays menu items, cart, totals, and printable receipts.
- Shows “No network, sale queued” if offline.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Flutter, Dart |
| **Backend** | FastAPI, Python |
| **Database** | SQLite |
| **Mock API** | FastAPI (for testing invoice submission) |
| **Tools** | Android Studio, VS Code, GitHub, Postman |

---

## 💾 Database Schema
Core tables:
- `products` – menu items with prices and tax rates  
- `sales` – transaction summaries  
- `sale_items` – line items linked to each sale  
- `invoice_logs` – stored requests and responses for tax submissions  

Seed data and schema are included in [`pos_schema_and_seed.sql`](./pos_schema_and_seed.sql).

---

## 🚀 Running the Project

### **Backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
sqlite3 pos.db < ../pos_schema_and_seed.sql
uvicorn app.main:app --reload
