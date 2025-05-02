from utils.db import query_db, insert_db

class AuthRepository:
    def find_user_by_username_or_email(self, username, email):
        return query_db(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username, email),
            one=True
        )
    
    def find_user_by_username(self, username):
        return query_db(
            'SELECT * FROM users WHERE username = ?',
            (username,),
            one=True
        )
    
    def find_user_by_id(self, user_id):
        return query_db(
            'SELECT * FROM users WHERE user_id = ?',
            (user_id,),
            one=True
        )
    
    def create_user(self, username, email, password_hash):
        return insert_db(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
    
    def create_default_categories(self, user_id, category_names):
        for category in category_names:
            insert_db(
                'INSERT INTO categories (user_id, name) VALUES (?, ?)',
                (user_id, category)
            )