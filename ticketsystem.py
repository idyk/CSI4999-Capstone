from nicegui import ui
import sqlite3
import pandas as pd

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')

df_tickets = pd.read_sql_query("SELECT * from Tickets", db_tickets)


@ui.page('/tables_page')
def tables_page():
    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40')
    ui.button('Toggle Grid', on_click=lambda: toggleGrid())

    def toggleGrid():
        if (grid.visible):
            print("grid is visible, hiding")
            grid.set_visibility(False)
        else:
            print("grid isn't visible, showing")
            grid.set_visibility(True)


def login_page():
    ui.label("Welcome to Ticket System! (name pending)")
    ui.label("Please login with your credentials.")

    username = ui.input(label="Username")
    password = ui.input(label="Password")

    ui.button("Sign in", on_click=lambda: attemptLogin())

    def attemptLogin():
        usernameSqlQueryCheck = pd.read_sql_query(
            "SELECT Username FROM Logins WHERE Username = '" + username.value + "'", db_login)
        passwordSqlQueryCheck = pd.read_sql_query(
            "SELECT Password FROM Logins WHERE Password = '" + password.value + "'", db_login)

        if (username.value == usernameSqlQueryCheck.at[0, 'Username']):
            print("Username correct")
            if (password.value == passwordSqlQueryCheck.at[0, 'Password']):
                print("Username and password correct, signing in")
                ui.open(tables_page)

    ui.link('Login', tables_page)


login_page()

ui.run()
