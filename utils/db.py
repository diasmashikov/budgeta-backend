import sqlite3
from flask import g, current_app
import click
from flask.cli import with_appcontext

def get_db():
    # Connect to the database
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def query_db(query, args=(), one=False):
    # Execute a query and return the results
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    # Insert data and return the ID
    db = get_db()
    cur = db.execute(query, args)
    last_id = cur.lastrowid
    db.commit()
    cur.close()
    return last_id

def update_db(query, args=()):
    # Update data and return rows affected
    db = get_db()
    cur = db.execute(query, args)
    affected = cur.rowcount
    db.commit()
    cur.close()
    return affected

def init_app(app):
    # Register database functions with the app
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)