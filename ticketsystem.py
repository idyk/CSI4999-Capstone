from nicegui import ui
from middleware_pages import start_page

import sqlite3
import pandas as pd
import datetime

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')

# The page that the user will see on first launch.
start_page()
ui.run(title="TICKSTER - IT Ticketing System", favicon="✔")
