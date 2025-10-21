from fastapi import FastAPI 
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
app = FastAPI()
#database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        cursor_factory=RealDictCursor
    )
    return conn

#creating  expenses 
@app.post("/expenses")
def add_expense(description: str, amount: float, category: str,date:str):
    conn =get_db_connection() # gets a connection object to my database
    cur = conn.cursor() #lets me send SQL commands through my open connection
    cur.execute(
        "INSERT INTO expenses(description,amount,category,date) VALUES (%s, %s, %s, %s) RETURNING * ",
        (description,amount,category,date)
    ) #executes an SQL command to insert a new expense record into the expenses table
    expense= cur.fetchone() #retrieves that single row and stores it in the variable expense
    conn.commit() #tells the database to save (commit) the transaction
    cur.close() #closing the cursor to free up memory and avoid resource leaks
    conn.close()

    return expense

#reading expenses
@app.get("/expenses")
def get_expenses():
   conn = get_db_connection()
   cur=conn.cursor() 
   cur.execute("SELECT * FROM expenses")
   expenses = cur.fetchall()

   cur.close()
   conn.close()

   return expenses

#getting the totals of expenses
@app.get("/expenses/total")
def get_totalexpenses():
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute( "SELECT SUM(amount) as total FROM expenses")
   result = cur.fetchone()
   cur.close()
   conn.close()
    
   return {"total":result['total'] or 0}

#deleting expenses
@app.delete("/expenses/{expenses_id}")
def delete_expenses(expenses_id: int):
    conn= get_db_connection()
    cur= conn.cursor()
    
    cur.execute("DELETE FROM expenses WHERE id = %s RETURNING *",(expenses_id,))
    deleted =cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return{"message": "Expense deleted successfully"}
    return{"error": "Expense not found"}

#updating expenses
@app.put("/expenses/{expenses_id}")
def update_expenses(expenses_id:int,description:str, amount: float,category: str, date:str):
   conn= get_db_connection()
   cur =conn.cursor()
   cur.execute("UPDATE expenses SET description =%s, amount = %s,category =%s, date= %s WHERE id= %s RETURNING * ",
               (description,amount,category,date,expenses_id)
   )
   updated= cur.fetchone()
   conn.commit()
   cur.close()
   conn.close()

   if updated:
    return updated
   return{"error":"Expense not found"}

#daily expenses summary
@app.get("/expenses/summary/today")
def get_today_total():
   conn =get_db_connection()
   cur= conn.cursor()
   cur.execute("""
       SELECT SUM(amount) as total
       FROM expenses
       WHERE date=CURRENT_DATE
    """)
   result= cur.fetchone()
   cur.close()
   conn.close()

   return{"period": "today","total": result['total'] or 0}

#weekly expenses summary    
@app.get("/expenses/summary/weekly")
def get_weekly_total():
   conn=get_db_connection()
   cur=conn.cursor()
   cur.execute("""
       SELECT SUM(amount) as weekly_total
       FROM expenses
       WHERE date >= CURRENT_DATE - INTERVAL'7 days'
     """) 
   result= cur.fetchone()
   cur.close()
   conn.close()

   return{"period":"weekly", "weekly_total":result['weekly_total'] or 0}
    
#monthly summary expenses
@app.get("/expenses/summary/monthly")
def get_monthly_total():
   conn=get_db_connection()
   cur=conn.cursor()
   cur.execute("""
        SELECT SUM(amount) AS monthly_total
        FROM expenses
        WHERE date >= date_trunc('month',CURRENT_DATE)       
                      
     """)
   result=cur.fetchone()
   cur.close()
   conn.close()
     
   return{"period":"monthly","total":result['monthly_total']or 0}

# getting all budgets
@app.get("/budgets")
def get_budgets():
   conn=get_db_connection()
   cur=conn.cursor()

   cur.execute("SELECT * FROM budgets")
   budgets=cur.fetchall()
   cur.close()
   conn.close()
   return budgets


#comparison between budget and the actual spending
@app.get("/budgets/status")
def get_budget_status():
   conn = get_db_connection()
   cur =conn.cursor()

   cur.execute(""" 
       SELECT
          b.category,
          b.monthly_limit,
          COALESCE(SUM(e.amount),0) as spent,
          b.monthly_limit - COALESCE(SUM(e.amount),0) AS remaining
       FROM budgets b
       LEFT JOIN expenses e
          ON b.category = e.category
          AND e.date >= date_trunc('month' ,CURRENT_DATE) 
        GROUP BY  b.category, b.monthly_limit                                           
    """)
   results = cur.fetchall()
   cur.close()
   conn.close()

#adding over_budget flag
   status =[]
   for row in results:
       status.append({
          "category": row['category'],
          "limit":row['monthly_limit'],
          "spent": row['spent'],
          "remaining":row['remaining'],
          "over_budget":row['remaining'] < 0

      }) 
   return status     


#creating budgets
@app.post("/budgets")
def add_budget(category: str,monthly_limit:float):
   conn=get_db_connection()
   cur=conn.cursor()
   cur.execute("INSERT INTO budgets(category,monthly_limit) VALUES(%s ,%s) RETURNING *",
               (category,monthly_limit)
         )
   budget=cur.fetchone()
   conn.commit()
   cur.close()
   conn.close()
   return budget





     
   
    



