from nicegui import ui
from middleware_pages import start_page
from nicegui import ui
import sqlite3
import pandas as pd

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')

start_page()
ui.run(title="TICKSTER - IT Ticketing System", favicon="✔")
