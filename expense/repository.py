from utils.db import query_db, insert_db, update_db
from datetime import datetime, date
import calendar

class ExpenseRepository:
    def get_expenses(self, user_id, month=None, year=None, category_id=None):
        query = '''
            SELECT e.*, c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = ?
        '''
        
        args = [user_id]
        
        if month and year:
            query += ' AND strftime("%m", e.date) = ? AND strftime("%Y", e.date) = ?'
            args.extend([f'{month:02d}', str(year)])
        elif month:
            query += ' AND strftime("%m", e.date) = ?'
            args.append(f'{month:02d}')
        elif year:
            query += ' AND strftime("%Y", e.date) = ?'
            args.append(str(year))
        
        if category_id:
            query += ' AND e.category_id = ?'
            args.append(category_id)
        
        query += ' ORDER BY e.date DESC, e.created_at DESC'
        
        expenses = query_db(query, tuple(args))
        return [dict(expense) for expense in expenses]
    
    def get_expense_by_id(self, user_id, expense_id):
        expense = query_db('''
            SELECT e.*, c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.expense_id = ? AND e.user_id = ?
        ''', (expense_id, user_id), one=True)
        
        return dict(expense) if expense else None
    
    def get_category(self, user_id, category_id):
        return query_db('''
            SELECT * FROM categories 
            WHERE category_id = ? AND user_id = ?
        ''', (category_id, user_id), one=True)
    
    def create_expense(self, user_id, category_id, amount, expense_date, description=None):
        return insert_db('''
            INSERT INTO expenses (user_id, category_id, amount, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category_id, amount, expense_date, description))
    
    def update_expense(self, user_id, expense_id, category_id=None, amount=None, expense_date=None, description=None):
        expense = self.get_expense_by_id(user_id, expense_id)
        if not expense:
            return False
        
        category_id = category_id if category_id is not None else expense['category_id']
        amount = amount if amount is not None else expense['amount']
        expense_date = expense_date if expense_date is not None else expense['date']
        description = description if description is not None else expense['description']
        
        rows_affected = update_db('''
            UPDATE expenses
            SET category_id = ?, amount = ?, date = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE expense_id = ? AND user_id = ?
        ''', (category_id, amount, expense_date, description, expense_id, user_id))
        
        return rows_affected > 0
    
    def delete_expense(self, user_id, expense_id):
        rows_affected = update_db('''
            DELETE FROM expenses
            WHERE expense_id = ? AND user_id = ?
        ''', (expense_id, user_id))
        
        return rows_affected > 0
    
    def calculate_total_amount(self, expenses):
        total = 0.0
        for expense in expenses:
            total += float(expense['amount'])
        return total
    
    def get_monthly_expenses_by_category(self, user_id, month, year):
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        query = '''
            SELECT e.category_id, c.name AS category_name, SUM(e.amount) AS total
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = ? AND e.date BETWEEN ? AND ?
            GROUP BY e.category_id
            ORDER BY total DESC
        '''
        
        expenses = query_db(query, (user_id, start_date, end_date))
        return [dict(expense) for expense in expenses]
    
    def get_recent_expenses(self, user_id, limit=5):
        query = '''
            SELECT e.*, c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = ?
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT ?
        '''
        
        expenses = query_db(query, (user_id, limit))
        return [dict(expense) for expense in expenses]