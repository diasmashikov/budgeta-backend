from utils.db import query_db, insert_db, update_db
from datetime import datetime

class IncomeRepository:
    def get_incomes(self, user_id, month=None, year=None):
        query = '''
            SELECT * FROM income_sources
            WHERE user_id = ?
        '''
        
        args = [user_id]
        
        if month and year:
            query += ' AND month = ? AND year = ?'
            args.extend([month, year])
        elif month:
            query += ' AND month = ?'
            args.append(month)
        elif year:
            query += ' AND year = ?'
            args.append(year)
        
        query += ' ORDER BY due_date ASC, source_name ASC'
        
        incomes = query_db(query, tuple(args))
        return [dict(income) for income in incomes]
    
    def get_income_by_id(self, user_id, income_id):
        income = query_db('''
            SELECT * FROM income_sources
            WHERE income_id = ? AND user_id = ?
        ''', (income_id, user_id), one=True)
        
        return dict(income) if income else None
    
    def create_income(self, user_id, source_name, expected_amount, month, year, due_date=None, description=None):
        return insert_db('''
            INSERT INTO income_sources (
                user_id, source_name, expected_amount, due_date, 
                month, year, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, source_name, expected_amount, due_date,
            month, year, description
        ))
    
    def update_income(self, user_id, income_id, source_name=None, expected_amount=None, 
                     actual_amount=None, is_received=None, due_date=None, 
                     receive_date=None, month=None, year=None, description=None):
        
        income = self.get_income_by_id(user_id, income_id)
        if not income:
            return False
        
        source_name = source_name if source_name is not None else income['source_name']
        expected_amount = expected_amount if expected_amount is not None else income['expected_amount']
        actual_amount = actual_amount if actual_amount is not None else income['actual_amount']
        is_received = is_received if is_received is not None else income['is_received']
        due_date = due_date if due_date is not None else income['due_date']
        receive_date = receive_date if receive_date is not None else income['receive_date']
        month = month if month is not None else income['month']
        year = year if year is not None else income['year']
        description = description if description is not None else income['description']
        
        rows_affected = update_db('''
            UPDATE income_sources
            SET source_name = ?, expected_amount = ?, actual_amount = ?,
                is_received = ?, due_date = ?, receive_date = ?,
                month = ?, year = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE income_id = ? AND user_id = ?
        ''', (
            source_name, expected_amount, actual_amount,
            is_received, due_date, receive_date,
            month, year, description,
            income_id, user_id
        ))
        
        return rows_affected > 0
    
    def delete_income(self, user_id, income_id):
        rows_affected = update_db('''
            DELETE FROM income_sources
            WHERE income_id = ? AND user_id = ?
        ''', (income_id, user_id))
        
        return rows_affected > 0
    
    def receive_income(self, user_id, income_id, actual_amount, receive_date=None):
        if receive_date is None:
            from datetime import date
            receive_date = date.today().isoformat()
        
        rows_affected = update_db('''
            UPDATE income_sources
            SET actual_amount = ?, is_received = TRUE, receive_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE income_id = ? AND user_id = ?
        ''', (actual_amount, receive_date, income_id, user_id))
        
        return rows_affected > 0
    
    def calculate_income_totals(self, incomes):
        total_expected = 0.0
        total_received = 0.0
        
        for income in incomes:
            total_expected += float(income['expected_amount'])
            
            if income['is_received'] and income['actual_amount']:
                total_received += float(income['actual_amount'])
        
        return total_expected, total_received