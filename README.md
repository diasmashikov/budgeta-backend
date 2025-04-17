# Budgeta Backend Development Guide



## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Database Operations](#database-operations)
- [Git Workflow](#git-workflow)

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Git
- Postman (optional, but recommended for API testing)
- Python 3.8+

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/diasmashikov/budgeta-backend.git
cd budgeta-tracker
```

### 2. Install necessary libraries
```bash
make load-libs # first time only
```


### 3. Start the Application

```bash
# Build and start the application
make init-db # first time only
make run
```

These commands will:
- Start the Flask application
- Create and initialize the SQLite database with the schema

### 3. Verify the Setup

The Flask application should now be running at `http://localhost:5001`. You can test if it's working by sending a request to register a user:

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

## Project Structure

```
budget_tracker/
│
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── schema.sql              # Database schema
├── requirements.txt        # Project dependencies
│
├── api/                    # API endpoints
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── categories.py       # Categories routes (to be implemented)
│   ├── income.py           # Income routes (to be implemented)
│   └── ...                 # Other API modules
│
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── auth.py             # Authentication utilities
│   └── db.py               # Database utilities
│
```

## Development Guide

### Creating a New API Module

To implement a new feature, start by creating a new file or modifying an existing one in the `api` directory:

```python
# api/categories.py
from flask import Blueprint, request, jsonify
from utils.db import query_db, insert_db, update_db
from utils.auth import token_required

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
@token_required
def get_categories(current_user):
    """Get all categories for the current user."""
    categories = query_db(
        'SELECT * FROM categories WHERE user_id = ?',
        (current_user['user_id'],)
    )
    
    return jsonify({
        'status': 'success',
        'categories': [dict(category) for category in categories]
    })

# Add more routes as needed
```

### Registering the Blueprint

After creating your module, register the blueprint in `app.py`:

```python
# In app.py, add to the create_app function
from api.categories import categories_bp
app.register_blueprint(categories_bp, url_prefix='/api/categories')
```

## Database Operations

The project uses raw SQL queries through the utility functions in `utils/db.py`:

- `query_db()` - For SELECT queries
- `insert_db()` - For INSERT queries
- `update_db()` - For UPDATE/DELETE queries

Example usage:

```python
# Select data
user = query_db('SELECT * FROM users WHERE username = ?', ('username',), one=True)

# Insert data
user_id = insert_db(
    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
    ('username', 'email@example.com', 'hashed_password')
)

# Update data
update_db(
    'UPDATE users SET email = ? WHERE user_id = ?',
    ('new_email@example.com', user_id)
)
```

When you make changes to your code, the development server automatically reloads thanks to the volume mapping in Docker Compose. You don't need to restart the container for most code changes.

## Git Workflow

### 1. Setting Up Your Branch

Always start with the latest code from the main branch:

```bash
# Make sure you're on the main branch:
git checkout main

# Pull the latest changes
git pull origin main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

Name your branch with a descriptive prefix:
- `feature/` for new features
- `bugfix/` for bug fixes

### 2. Developing Your Feature

As you work on your feature:

```bash
# Check what files you've modified
git status

# Add your changes
git add file1.py file2.py
# Or add all changes
git add .

# Commit your changes with a descriptive message
git commit -m "Add category creation functionality"
```

### 3. Syncing with Main Branch

If development on main continues while you're working on your feature:

```bash
# Save your current changes
git add .
git commit -m "WIP: Save progress on feature"

# Switch to main and get updates
git checkout main
git pull origin main

# Switch back to your branch
git checkout feature/your-feature-name

# Merge the latest changes from main
git merge main

# Resolve any conflicts if necessary
```

### 4. Pushing Your Changes

When you're ready to share your work:

```bash
# Push your branch to the remote repository
git push -u origin feature/your-feature-name
```

### 5. Creating a Pull Request (PR)

- Go to the repository on GitHub
- Click "New Pull Request" or "Create Merge Request"
- Select your branch as the source
- Add a descriptive title and detailed description
- Reference any related issues (#123)
- Request reviews from team members
- Submit the PR

### 6. Addressing Review Comments

After receiving feedback:

```bash
# Make the requested changes
git add .
git commit -m "Address PR feedback: improve error handling"

# Push the changes to update the PR
git push origin feature/your-feature-name
```

### 7. Merging Your PR

Once approved, merge your PR (through the web interface or via commands if you have permission).
After merging, clean up:

```bash
# Switch back to main
git checkout main

# Pull the updated main that includes your changes
git pull origin main

# Delete your local branch
git branch -d feature/your-feature-name
```