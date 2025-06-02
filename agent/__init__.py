from datetime import datetime
import json
import sqlite3
from google.adk.agents import Agent

db = sqlite3.connect("database.db")

def create_transaction(date: str, amount: float, category: str, description: str = "") -> dict:
    """
    Creates a new transaction in the database.
    Args:
        date (str): Transaction date in YYYY-MM-DD format
        amount (float): Transaction amount
        category (str): Category name
        description (str): Transaction description
    Returns:
        dict: Status of the operation
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO transactions (date, amount, category, description) VALUES (?, ?, ?, ?)",
            (date, amount, category, description)
        )
        db.commit()
        return {"status": "success", "message": "Transaction created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_monthly_spending(month: str, year: int) -> dict:
    """
    Retrieves total spending for a specific month and year.
    Args:
        month (str): Month in MM format
        year (int): Year in YYYY format
    Returns:
        dict: Monthly spending summary
    """
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
        """, (month, str(year)))
        results = cursor.fetchall()
        return {
            "status": "success",
            "data": [{"category": r[0], "total": r[1]} for r in results]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_spending_history(category: str = "", start_date: str = "", end_date: str = "") -> dict:
    """
    Analyzes spending history with optional filters.
    Args:
        category (str): Filter by category
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    Returns:
        dict: Analysis results
    """
    try:
        cursor = db.cursor()
        query = "SELECT date, amount, category, description FROM transactions WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            
        query += " ORDER BY date DESC"
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return {
            "status": "success",
            "data": [
                {
                    "date": r[0],
                    "amount": r[1],
                    "category": r[2],
                    "description": r[3]
                } for r in results
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_current_date() -> dict:
    """
    Gets the current date in YYYY-MM-DD format.
    Returns:
        dict: Current date information
    """
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return {
            "status": "success",
            "data": current_date
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


root_agent = Agent(
    name="financial_data_agent",
    model="gemini-1.5-flash",
    description=(
        "You are an agent to help with processing personal financial data."
    ),
    instruction=(
        """
        You are a helpful agent who can answer user questions about their personal financial data.
        You can use the following tools to help you:
        - create_transaction: to create a new transaction in the database.
        - get_monthly_spending: to get the monthly spending for a specific month and year.
        - analyze_spending_history: to analyze the spending history with optional filters.
        - get_current_date: to get the current date in YYYY-MM-DD format.
        """
    ),
    tools=[create_transaction, get_monthly_spending, analyze_spending_history, get_current_date],
)