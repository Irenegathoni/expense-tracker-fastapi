# Expense Tracker API

A backend application built with **FastAPI** and **PostgreSQL** for managing expenses and budgets.  
It provides RESTful endpoints for creating, updating, and analyzing financial data, supporting both personal and organizational use.  
The project demonstrates strong backend engineering practices, clean architecture, and structured database interaction.

---

## Features
- Create, read, update, and delete expense records  
- Define and manage category-based budgets  
- Generate daily, weekly, and monthly expense summaries  
- Compare actual spending against allocated budgets  
- Environment variable management using `python-dotenv`

---

## Tech Stack
- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** PostgreSQL  
- **Driver:** psycopg2  
- **Environment Management:** python-dotenv  

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/irenegathoni/expense-tracker-fastapi.git
   cd expense-tracker-fastapi
2. **Create a virtual environment**
   ```bash
    python -m venv venv

  
On Windows

venv\Scripts\activate
On macOS / Linux
 
source venv/bin/activate

3.**Install dependencies**
pip install -r requirements.txt

4. **Configure environment variables**

Create a .env file in the project root using .env.example as a template:

PGHOST=your_database_host
PGDATABASE=your_database_name
PGUSER=your_database_user
PGPASSWORD=your_database_password

5.**Run the application**
uvicorn main2:app --reload

6.**Access API documentation**

Open your browser and navigate to:
http://127.0.0.1:8000/docs
--
**Database Schema**
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    description TEXT,
    amount FLOAT,
    category TEXT,
    date DATE
);

CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    category TEXT,
    monthly_limit FLOAT
);
--
**Example Endpoints**
Method	Endpoint	Description
POST	/expenses	Add a new expense
GET	/expenses	Retrieve all expenses
PUT	/expenses/{id}	Update an existing expense
DELETE	/expenses/{id}	Delete an expense
GET	/expenses/summary/today	Daily spending summary
GET	/expenses/summary/weekly	Weekly spending summary
GET	/expenses/summary/monthly	Monthly spending summary
POST	/budgets	Add a new budget
GET	/budgets/status	Compare budgets vs spending
--
**Future Enhancements**

Implement JWT authentication for secure user access

Add user registration and multi-account support

Include analytics dashboard integration (Streamlit or Plotly)

Containerize with Docker and deploy to cloud platforms

Optimize query performance with caching
   git clone https://github.com/irenegathoni/expense-tracker-fastapi.git
   cd expense-tracker-fastapi
