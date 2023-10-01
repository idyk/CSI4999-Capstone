from nicegui import ui
import sqlite3
import pandas as pd
import datetime

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')

# The page that the user will see on first launch.


@ui.page('/login_page')
def login_page():
    ui.label("Welcome to Ticket System! (name pending)")
    ui.label("Please login with your credentials.")

    username = ui.input(label="Username")
    password = ui.input(label="Password")

    ui.button("Sign in", on_click=lambda: attemptLogin())

    # This checks the username and password against the login database for validation. It will also check if the user is elevated or not to
    # direct them to the correct set of pages.
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


# This lets us set the username. Not sure if it's even needed but yeah...
def setUsername(user):
    print("setting global username to: " + user)
    global username
    username = user

# First nonadmin page. Has create ticket and view ticket buttons.


@ui.page('/nonadmin_page')
def nonadmin_page():
    ui.label("This is the nonadmin view.")
    ui.button("Logout", on_click=lambda: ui.open(login_page))
    ui.button("Create Ticket", on_click=lambda: ui.open(nonadmin_ticket_create))
    ui.button("View Created Tickets", on_click=lambda: ui.open(
        nonadmin_ticket_view_list))

# Creating a ticket as a nonadmin page. Lets user type title and issue, and then when they submit,
# it will auto generate the next ticket number, as well as a timestamp.
# It will default to No Assignee and Open until someone on Admin side takes control of ticket.


@ui.page("/nonadmin_ticket_create")
def nonadmin_ticket_create():

    ui.button("Go back", on_click=lambda: ui.open(nonadmin_page))
    ui.label("Nonadmin - Create Ticket")
    ui.label("Title:")
    ticketTitle = ui.textarea("Enter your issue's title here.")
    ui.label("Issue:")
    ticketDesc = ui.textarea("Enter your issue's description here.")
    ui.button("Submit", on_click=lambda: submitTicket())

    def submitTicket():
        global username
        maxIndexOfTicketNumber = pd.read_sql_query(
            "SELECT MAX(TicketNumber) FROM Tickets", db_tickets)
        indexToUse = maxIndexOfTicketNumber.at[0, 'MAX(TicketNumber)']+1
        print("Inserting into index " + str(indexToUse) +
              " with the following information: ")
        print(ticketTitle.value)
        print(ticketDesc.value)
        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)
        cursor = db_tickets.cursor()
        cursor.execute("INSERT INTO Tickets (TicketNumber, Title, Description, Timestamp, Assignee, Status, User) VALUES ('" + str(indexToUse) +
                       "', '" + str(ticketTitle.value) + "', '" + str(ticketDesc.value) + "', '" + str(realTicketTimeStamp) + "', 'No Assignee', 'Open', '" + username + "')")
        db_tickets.commit()
        cursor.close()
        ui.open(nonadmin_page)

# This lets the user view their tickets list by ticket number and title only.


@ui.page("/nonadmin_ticket_view_list")
def nonadmin_ticket_view_list():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_page))

    global username

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title from Tickets WHERE User = '" + username + "'", db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40')
    grid.set_visibility(True)

    ticketNumbersSqlQueryGet = pd.read_sql_query(
        "SELECT TicketNumber FROM Tickets WHERE User = '" + username + "'", db_tickets)

    # This creates a dropdown for the user to pick from which ticket they would like to view further information on.
    arrayOfTicketNumbers = []
    for i in range(0, len(ticketNumbersSqlQueryGet), 1):
        print("One of " + str(username) + "'s Ticket Numbers: " +
              str(ticketNumbersSqlQueryGet.at[i, 'TicketNumber']))
        arrayOfTicketNumbers.append(
            ticketNumbersSqlQueryGet.at[i, 'TicketNumber'])

    global queriedTicketNumber
    ui.label(
        "Select the ticket from the dropdown to see more information on it.")
    queriedTicketNumber = ui.select(options=arrayOfTicketNumbers,
                                    on_change=lambda: ui.open(nonadmin_ticket_view_info))

# This will show further information. There is also another button to view even more details.


@ui.page("/nonadmin_ticket_view_info")
def nonadmin_ticket_view_info():
    global queriedTicketNumber

    print("Showing Ticket " + str(queriedTicketNumber.value) + ".")
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_ticket_view_list))

    ticketNumber = queriedTicketNumber.value

    ticketTitle = pd.read_sql_query(
        "SELECT Title from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketDesc = pd.read_sql_query(
        "SELECT Description from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketAssignee = pd.read_sql_query(
        "SELECT Assignee from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ui.label("Ticket #" + str(ticketNumber))
    ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
    ui.label("Ticket Description: " + ticketDesc.at[0, "Description"])

    ui.button("View further information", on_click=lambda: ui.open(
        nonadmin_ticket_view_more_info))

    ui.label("If you'd like to make changes to your ticket, feel free to do so.")
    ticketTitle = ui.textarea("Update title.")
    # ui.label("Issue:")
    ticketDesc = ui.textarea("Update description.")
    ui.button("Submit", on_click=lambda: updateTicket())

    def updateTicket():
        global username
        indexToUse = ticketNumber
        print("Updating into index " + str(indexToUse) +
              " with the following information: ")
        print(ticketTitle.value)
        print(ticketDesc.value)
        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)
        cursor = db_tickets.cursor()
        cursor.execute("UPDATE Tickets SET Title = '" + str(ticketTitle.value) + "', Description = '" + str(ticketDesc.value) + "', Assignee = '" + str(ticketAssignee.at[0, "Assignee"]) +
                       "', Status = 'Open', Timestamp = '" + str(realTicketTimeStamp) + "' WHERE TicketNumber = '" + str(ticketNumber) + "'")
        db_tickets.commit()
        cursor.close()

        cursor = db_history.cursor()
        indexOfHistoryNumber = pd.read_sql_query(
            "SELECT MAX(HistoryID) FROM TicketHistory", db_history)
        indexOfHistoryNumber += 1

        print("HISTORY ID IS: " +
              str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]))
        cursor.execute("INSERT INTO TicketHistory (HistoryID, TicketNumber, Username, Assignee, Description, Timestamp) VALUES ('" + str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]) +
                       "', '" + str(ticketNumber) + "', '" + str(username) + "', '" + str(ticketAssignee.at[0, "Assignee"]) + "', '" + str(ticketDesc.value) + "', '" + str(realTicketTimeStamp) + "')")

        db_history.commit()
        cursor.close()

        ui.open(nonadmin_page)


# This shows more information that isn't really needed to know for the user, but they may want to see it still.


@ui.page("/nonadmin_ticket_view_more_info")
def nonadmin_ticket_view_more_info():
    ui.button("Go back", on_click=lambda: ui.open(nonadmin_ticket_view_info))

    global queriedTicketNumber
    ticketNumber = queriedTicketNumber.value

    ticketTimestamp = pd.read_sql_query(
        "SELECT Timestamp from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketAssignee = pd.read_sql_query(
        "SELECT Assignee from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketStatus = pd.read_sql_query(
        "SELECT Status from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ui.label("Time Created: " + ticketTimestamp.at[0, "Timestamp"])
    ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
    ui.label("Ticket Staus: " + ticketStatus.at[0, "Status"])


# ADMIN VIEW SECTION

@ui.page('/admin_page')
def admin_page():
    ui.label("This is the admin view.")
    ui.button("Logout", on_click=lambda: ui.open(login_page))
    ui.button("View Created Tickets", on_click=lambda: ui.open(
        admin_ticket_view_list))


@ui.page("/admin_ticket_view_list")
def admin_ticket_view_list():
    ui.button("Go back", on_click=lambda: ui.open(admin_page))

    global username

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title from Tickets", db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40')
    grid.set_visibility(True)

    ticketNumbersSqlQueryGet = pd.read_sql_query(
        "SELECT TicketNumber FROM Tickets", db_tickets)

    # This creates a dropdown for the user to pick from which ticket they would like to view further information on.
    arrayOfTicketNumbers = []
    for i in range(0, len(ticketNumbersSqlQueryGet), 1):
        arrayOfTicketNumbers.append(
            ticketNumbersSqlQueryGet.at[i, 'TicketNumber'])

    global queriedTicketNumber
    ui.label(
        "Select the ticket from the dropdown to see more information on it.")
    queriedTicketNumber = ui.select(options=arrayOfTicketNumbers,
                                    on_change=lambda: ui.open(admin_ticket_view_info))


@ui.page("/admin_ticket_view_info")
def admin_ticket_view_info():
    global queriedTicketNumber

    print("Showing Ticket " + str(queriedTicketNumber.value) + ".")
    ui.button("Go back", on_click=lambda: ui.open(admin_ticket_view_list))

    ticketNumber = queriedTicketNumber.value

    elevatedUserGet = pd.read_sql_query(
        "SELECT Username FROM Logins WHERE Elevated = 'True'", db_login)

    print("elevated length: " + str(len(elevatedUserGet)))

    ticketTitle = pd.read_sql_query(
        "SELECT Title from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketDesc = pd.read_sql_query(
        "SELECT Description from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketTimestamp = pd.read_sql_query(
        "SELECT Timestamp from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketAssignee = pd.read_sql_query(
        "SELECT Assignee from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketStatus = pd.read_sql_query(
        "SELECT Status from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketUsername = pd.read_sql_query(
        "SELECT User from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ui.label("Ticket #" + str(ticketNumber))
    ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
    ui.label("Ticket Description: " + ticketDesc.at[0, "Description"])
    ui.label("Time Created: " + ticketTimestamp.at[0, "Timestamp"])
    ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
    ui.label("Ticket Staus: " + ticketStatus.at[0, "Status"])

    arrayOfAssignees = []
    for i in range(0, len(elevatedUserGet), 1):
        arrayOfAssignees.append(
            elevatedUserGet.at[i, 'Username'])

    # Default to first possible assignee in case of anything...
    selectedAssignee = ui.select(options=arrayOfAssignees, value=arrayOfAssignees[0],
                                 on_change=lambda: print("user selected"))

    arrayOfStatuses = ["Open", "Resolved", "On Hold"]
    selectedStatus = ui.select(options=arrayOfStatuses, value=arrayOfStatuses[0],
                               on_change=lambda: print("status selected"))

    ticketTitle = ui.textarea("Update title.")
    # ui.label("Issue:")
    ticketDesc = ui.textarea("Update description.")
    ui.button("Submit", on_click=lambda: updateTicket())

    def updateTicket():
        global username
        indexToUse = ticketNumber
        print("Updating into index " + str(indexToUse) +
              " with the following information: ")
        print(ticketTitle.value)
        print(ticketDesc.value)
        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)
        cursor = db_tickets.cursor()
        cursor.execute("UPDATE Tickets SET Title = '" + str(ticketTitle.value) + "', Description = '" + str(ticketDesc.value) + "', Assignee = '" + str(selectedAssignee.value) +
                       "', Status = '" + str(selectedStatus.value) + "', Timestamp = '" + str(realTicketTimeStamp) + "' WHERE TicketNumber = '" + str(ticketNumber) + "'")
        db_tickets.commit()
        cursor.close()

        cursor = db_history.cursor()
        indexOfHistoryNumber = pd.read_sql_query(
            "SELECT MAX(HistoryID) FROM TicketHistory", db_history)
        indexOfHistoryNumber += 1

        print("HISTORY ID IS: " +
              str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]))

        print("Username is " + str(ticketUsername))
        # cursor.execute("INSERT INTO TicketHistory (HistoryID, TicketNumber, Username, Assignee, Description, Timestamp) VALUES ('" + str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]) +
        #                "', '" + str(ticketNumber) + "', '" + str(ticketUsername[0, "Username"]) + "', '" + str(ticketAssignee.at[0, "Assignee"]) + "', '" + str(ticketDesc.value) + "', '" + str(realTicketTimeStamp) + "')")

        # db_history.commit()
        cursor.close()

        ui.open(admin_page)


login_page()
ui.run()
