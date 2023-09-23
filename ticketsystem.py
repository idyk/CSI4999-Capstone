from nicegui import ui
import sqlite3
import pandas as pd

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
# The page that the user will see on first launch.


@ui.page('/login_page')
def login_page():
    ui.label("Welcome to Ticket System! (name pending)")
    ui.label("Please login with your credentials.")

    username = ui.input(label="Username")
    password = ui.input(label="Password")

    # loginMessage = ui.label("")

    ui.button("Sign in", on_click=lambda: attemptLogin())

    def attemptLogin():
        usernameSqlQueryCheck = pd.read_sql_query(
            "SELECT Username FROM Logins WHERE Username = '" + username.value + "'", db_login)
        passwordSqlQueryCheck = pd.read_sql_query(
            "SELECT Password FROM Logins WHERE Password = '" + password.value + "'", db_login)
        elevatedSqlQueryCheck = pd.read_sql_query(
            "SELECT Elevated FROM Logins WHERE Username = '" + username.value + "'", db_login)

        if (username.value == usernameSqlQueryCheck.at[0, 'Username']):
            print("Username correct")
            setUsername(username.value)
            if (password.value == passwordSqlQueryCheck.at[0, 'Password']):
                print(
                    "Username and password correct, signing in with dependent elevation")
                if (elevatedSqlQueryCheck.at[0, 'Elevated'] == "False"):
                    ui.open(nonadmin_page)
                else:
                    ui.open(admin_page)


def setUsername(user):
    print("setting global username to: " + user)
    global username
    username = user


@ui.page('/nonadmin_page')
def nonadmin_page():
    ui.label("This is the nonadmin view.")
    ui.button("Create Ticket", on_click=lambda: ui.open(nonadmin_ticket_create))
    ui.button("View Created Tickets", on_click=lambda: ui.open(
        nonadmin_ticket_view_list))


@ui.page('/admin_page')
def admin_page():
    ui.label("Admin")


@ui.page("/nonadmin_ticket_create")
def nonadmin_ticket_create():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_page))
    ui.label("Nonadmin - Create Ticket")
    ui.label("Title:")
    ui.textarea("Enter your issue's title here.")
    ui.label("Issue:")
    ui.textarea("Enter your issue's description here.")
    ui.button("Submit")


queriedTicketNumber = "0"
queriedTitle = "default title"
queriedDescription = "default description"
queriedTimestamp = "00:00"
queriedAssignee = "default assignee"
queriedStatus = "default status"
queriedUser = "default user"


@ui.page("/nonadmin_ticket_view_list")
def nonadmin_ticket_view_list():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_page))

    global username
    username = "nonadmin"

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title from Tickets WHERE User = '" + username + "'", db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40')
    grid.set_visibility(True)

    ticketNumbersSqlQueryGet = pd.read_sql_query(
        "SELECT TicketNumber FROM Tickets WHERE User = '" + username + "'", db_tickets)

    for i in range(0, len(ticketNumbersSqlQueryGet), 1):
        print("One of " + str(username) + "'s Ticket Numbers: " +
              str(ticketNumbersSqlQueryGet.at[i, 'TicketNumber']))
        arrayOfTicketNumbers = ticketNumbersSqlQueryGet.at[i, 'TicketNumber']

    ui.label("Your issues can be viewed in more detail by pressing this button.")
    ui.button("TEMP BUTTON - View Empty Selected Ticket",
              on_click=lambda: ui.open(nonadmin_ticket_view_info))


@ui.page("/nonadmin_ticket_view_info")
def nonadmin_ticket_view_info():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_ticket_view_list))
    ui.button("View further information", on_click=lambda: ui.open(
        nonadmin_ticket_view_more_info))
    ui.label("Ticket number: " +
             queriedTicketNumber)
    ui.label("Ticket title: " + queriedTitle)
    ui.label("Ticket description: " + queriedDescription)


@ui.page("/nonadmin_ticket_view_more_info")
def nonadmin_ticket_view_more_info():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_ticket_view_info))
    ui.label("Timestamp: " + queriedTimestamp)
    ui.label("Assignee: " + queriedAssignee)
    ui.label("Status: " + queriedStatus)


login_page()
ui.run()
