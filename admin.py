from nicegui import ui
import sqlite3
import pandas as pd
import datetime
from login import *

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')


@ui.page('/admin_page')
def admin_page():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(242,125,119,1) 0%, rgba(244,122,77,1) 30%, rgba(235,225,150,1) 70%, rgba(214,130,32,1) 99%);
                background-size: 400% 400%;
                animation: gradient 5s ease infinite;
                height: 100vh;
            }}

        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        </style>
            """
    ui.html(backgroundHtml)

    ui.button("Logout", on_click=lambda: ui.open(
        login_page), icon="logout", color="red")
    with ui.row().classes('w-full justify-center'):
        with ui.column().classes('w-full items-center'):
            ui.label("Hello " + str(username) +
                     "!").style("font-size: 40px; font-weight: bold")
            ui.label("Please select from the options below.").style(
                "font-size: 25px;")
            ui.button("View Created Tickets", on_click=lambda: ui.open(
                admin_ticket_view_list), color="orange", icon="search").classes("py-2 px-4 rounded-full")
            ui.button("Create A User", on_click=lambda: ui.open(
                admin_create_user), color="pink", icon="add").classes("py-2 px-4 rounded-full")


@ui.page("/admin_create_user")
def admin_create_user():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(242,125,119,1) 0%, rgba(244,122,77,1) 30%, rgba(235,225,150,1) 70%, rgba(214,130,32,1) 99%);
                background-size: 400% 400%;
                animation: gradient 5s ease infinite;
                height: 100vh;
            }}

        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        </style>
            """
    ui.html(backgroundHtml)
    ui.button("Go back", on_click=lambda: ui.open(
        admin_page), color="red", icon="arrow_back")
    with ui.row().classes('w-2/3 border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin-left: auto; margin-right: auto; background-color: white'):
        with ui.column().classes('w-full items-center'):
            newUsername = ui.input(
                "Create username.").classes('w-50 items-center').style("text-align: center")
            newPassword = ui.input(
                "Create password.").classes('w-50')
            ui.label("Elevated?")
            elevationStatus = ui.select(options=["False", "True"])
            ui.button("Create User", on_click=lambda: generateUser(
                newUsername.value, newPassword.value, elevationStatus.value), color="green", icon="add_circle")

    def generateUser(usernameInput, passwordInput, elevationInput):

        checkUniqueUsername = pd.read_sql_query(
            "SELECT EXISTS(SELECT * FROM Logins WHERE Username = '" + str(usernameInput) + "')", db_login)

        if checkUniqueUsername.at[0, "EXISTS(SELECT * FROM Logins WHERE Username = '" + str(usernameInput) + "')"] == 1:
            print("Username already exists")
            ui.notify("Username already exists.",
                      type="negative", position="top")

        else:
            cursor = db_login.cursor()
            userID = pd.read_sql_query(
                "SELECT MAX(UserID) FROM Logins", db_login)
            userID += 1

            print("NEW USER ID IS: " +
                  str(userID.at[0, "MAX(UserID)"]))

            print("New username is " + str(usernameInput))
            cursor.execute("INSERT INTO Logins (UserID, Username, Password, Elevated) VALUES ('" + str(userID.at[0, "MAX(UserID)"]) +
                           "', '" + str(usernameInput) + "', '" + str(passwordInput) + "', '" + str(elevationInput) + "')")
            db_login.commit()
            cursor.close()
            ui.open(admin_page)


@ui.page("/admin_ticket_view_list")
def admin_ticket_view_list():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(242,125,119,1) 0%, rgba(244,122,77,1) 30%, rgba(235,225,150,1) 70%, rgba(214,130,32,1) 99%);
                background-size: 400% 400%;
                animation: gradient 5s ease infinite;
                height: 100vh;
            }}

        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        </style>
            """
    ui.html(backgroundHtml)
    ui.button("Go back", on_click=lambda: ui.open(
        admin_page), color="red", icon="arrow_back")

    global username

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title from Tickets", db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40').classes(
        'max-h-40 max-w-99')
    grid.set_visibility(True)

    ticketNumbersSqlQueryGet = pd.read_sql_query(
        "SELECT TicketNumber FROM Tickets", db_tickets)

    # This creates a dropdown for the user to pick from which ticket they would like to view further information on.
    arrayOfTicketNumbers = []
    for i in range(0, len(ticketNumbersSqlQueryGet), 1):
        arrayOfTicketNumbers.append(
            ticketNumbersSqlQueryGet.at[i, 'TicketNumber'])

    global queriedTicketNumber
    with ui.row().classes('w-full justify-center'):
        with ui.column().classes('w-full items-center'):
            ui.label(
                "Select the ticket from the dropdown to see more information on it, or to update it.").style(
                "font-size: 19px; font-weight: bold")
            queriedTicketNumber = ui.select(options=arrayOfTicketNumbers,
                                            on_change=lambda: ui.open(admin_ticket_view_info))


@ui.page("/admin_ticket_view_info")
def admin_ticket_view_info():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(242,125,119,1) 0%, rgba(244,122,77,1) 30%, rgba(235,225,150,1) 70%, rgba(214,130,32,1) 99%);
                background-size: 400% 400%;
                animation: gradient 5s ease infinite;
                height: 100vh;
            }}

        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        </style>
            """
    ui.html(backgroundHtml)
    global queriedTicketNumber

    print("Showing Ticket " + str(queriedTicketNumber.value) + ".")

    ticketNumber = queriedTicketNumber.value

    elevatedUserGet = pd.read_sql_query(
        "SELECT Username FROM Logins WHERE Elevated = 'True'", db_login)

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

    ticketHistoryDesc = pd.read_sql_query(
        "SELECT Description FROM TicketHistory WHERE TicketNumber = '" + str(ticketNumber) + "'", db_history)

    ticketHistoryTimestamp = pd.read_sql_query(
        "SELECT Timestamp FROM TicketHistory WHERE TicketNumber = '" + str(ticketNumber) + "'", db_history)

    ticketHistoryUpdater = pd.read_sql_query(
        "SELECT Updater FROM TicketHistory WHERE TicketNumber = '" + str(ticketNumber) + "'", db_history)

    ticketHistoryTitle = pd.read_sql_query(
        "SELECT Title FROM TicketHistory WHERE TicketNumber = '" + str(ticketNumber) + "'", db_history)

    ui.query('.nicegui-content').style('display: inline; padding: 0px')

    ui.button("Go back", on_click=lambda: ui.open(
        admin_ticket_view_list), color="red", icon="arrow_back")

    with ui.row().classes('border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Ticket #" + str(ticketNumber))
        ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
        ui.label("Last Updated: " + ticketTimestamp.at[0, "Timestamp"])
        ui.label("Ticket User: " + ticketUsername.at[0, "User"])
        ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
        ui.label("Ticket Status: " + ticketStatus.at[0, "Status"])

    with ui.column().classes('border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Current Ticket Description: ")
        ui.label(ticketDesc.at[0, "Description"])

    with ui.column().classes('justify-center items-center .p-12').style('text-align: center; padding: 20px; margin: 20px'):
        ui.button("Toggle History", color="red", icon="history", on_click=lambda: createHistory(
        )).style('font-weight: bold; text-align: center')

    container = ui.row().classes('w-full justify-center')

    def createHistory():
        if len(list(container)) > 0:
            print("clear")
            container.clear()
        else:
            print("fill")
            with container:
                with ui.column().classes('w-max items-center border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style("background-color: white;"):
                    for i in range(0, len(ticketHistoryDesc), 1):
                        ui.label("Ticket Description at " +
                                 ticketHistoryTimestamp.at[i, "Timestamp"] + " by " + ticketHistoryUpdater.at[i, "Updater"] + " with title " + ticketHistoryTitle.at[i, "Title"]).style('text-align: center; padding: 20px')
                        ui.label(ticketHistoryDesc.at[i, "Description"]).style(
                            'text-align: center; padding: 20px')

    arrayOfAssignees = []
    for i in range(0, len(elevatedUserGet), 1):
        arrayOfAssignees.append(
            elevatedUserGet.at[i, 'Username'])

    # Default to first possible assignee in case of anything...
    selectedAssignee = arrayOfAssignees[0]
    arrayOfStatuses = ["Open", "Resolved", "On Hold"]
    selectedStatus = arrayOfStatuses[0]

    with ui.column().classes('border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Update Assignee").style("font-size: 20px")
        selectedAssignee = ui.select(options=arrayOfAssignees, value=arrayOfAssignees[0],
                                     on_change=lambda: print("user selected")).classes('w-max')
        ui.label("Update Status").style("font-size: 20px")
        selectedStatus = ui.select(options=arrayOfStatuses, value=arrayOfStatuses[0],
                                   on_change=lambda: print("status selected")).classes('w-max')
        ticketTitle = ui.textarea(
            "Update title.").classes('w-full')
        ticketDesc = ui.textarea("Update description.").classes('w-full')
        ui.button("Submit", on_click=lambda: updateTicket(),
                  color="green", icon="done").style("margin-bottom: 20px")

    def updateTicket():
        global username
        indexToUse = ticketNumber
        print("Updating into index " + str(indexToUse) +
              " with the following information: ")
        print("Before cleanse: ", ticketTitle.value)
        title = str(ticketTitle.value).replace("'", "''")
        print("After cleanse: ", title)

        print("Before cleanse: ", ticketDesc.value)
        desc = str(ticketDesc.value).replace("'", "''")
        print("After cleanse: ", desc)

        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)
        if (len(ticketTitle.value) > 0 and len(ticketDesc.value) > 0):
            cursor = db_tickets.cursor()
            cursor.execute("UPDATE Tickets SET Title = '" + str(title) + "', Description = '" + str(desc) + "', Assignee = '" + str(selectedAssignee.value) +
                           "', Status = '" + str(selectedStatus.value) + "', Timestamp = '" + str(realTicketTimeStamp) + "' WHERE TicketNumber = '" + str(ticketNumber) + "'")
            db_tickets.commit()
            cursor.close()

            cursor = db_history.cursor()
            indexOfHistoryNumber = pd.read_sql_query(
                "SELECT MAX(HistoryID) FROM TicketHistory", db_history)
            indexOfHistoryNumber += 1

            print("HISTORY ID IS: " +
                  str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]))

            print("Username is " + str(ticketUsername.at[0, "User"]))
            cursor.execute("INSERT INTO TicketHistory (HistoryID, TicketNumber, Username, Assignee, Description, Timestamp, Updater, Title) VALUES ('" + str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]) +
                           "', '" + str(ticketNumber) + "', '" + str(ticketUsername.at[0, "User"]) + "', '" + str(ticketAssignee.at[0, "Assignee"]) + "', '" + str(desc) + "', '" + str(realTicketTimeStamp) + "', '" + str(username) + "', '" + str(title) + "')")

            db_history.commit()
            cursor.close()

            ui.open(admin_page)
        else:
            ui.notify(
                "No blank title or description updates permitted.", type="warning", position="top")
