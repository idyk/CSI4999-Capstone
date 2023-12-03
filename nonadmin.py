from nicegui import ui
import sqlite3
import pandas as pd
import datetime
from middleware_pages import open_login_page
from middleware_variables import getUsername

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')

username = getUsername()


def open_nonadmin():
    print("open nonadmin")
    ui.open(nonadmin_page)


@ui.page('/nonadmin_page')
def nonadmin_page():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%);
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
    # ui.query('body').style(
    #     ' background: rgb(199,233,191); background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%); ;')

    ui.button("Logout", on_click=lambda: open_login_page(), icon="logout",
              color="red").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    with ui.row().classes('w-full justify-center'):
        with ui.column().classes('w-full items-center'):
            ui.label("Hello " + str(username) +
                     "!").style("font-size: 40px; font-weight: bold").tailwind.animation('bounce')
            ui.label("Please select from the options below.").style(
                "font-size: 25px;")

            ui.button("Create Ticket", on_click=lambda: ui.open(
                nonadmin_ticket_create), color="green", icon="edit").classes("py-2 px-4 rounded-full").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black').gradient_color_stops('from-10%').justify_content('center')
            ui.button("View Created Tickets", on_click=lambda: ui.open(
                nonadmin_ticket_view_list), color="orange", icon="search").classes("py-2 px-4 rounded-full").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black').gradient_color_stops('from-10%').justify_content('center')


# Creating a ticket as a nonadmin page. Lets user type title and issue, and then when they submit,
# it will auto generate the next ticket number, as well as a timestamp.
# It will default to No Assignee and Open until someone on Admin side takes control of ticket.

# --------------------


@ui.page("/nonadmin_ticket_create")
def nonadmin_ticket_create():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%);
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
        nonadmin_page), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    with ui.row().classes('w-full justify-center border-indigo border-width-thick'):
        with ui.column().classes('w-full items-center border-indigo border-width-thick'):
            ui.label("Create your ticket, " + str(username) + "!").tailwind.font_size('2xl').font_weight(
                'bold').text_color('black').outline_color('white').outline_width('1').drop_shadow('lg')
            ticketTitle = ui.textarea(
                "Enter your issue's title here.").classes('w-10/12 border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white')
            ui.label("Issue Type").style("font-size: 20px")
            ticketType = ui.toggle({1: 'Software', 2: 'Hardware'})
            ui.label("Priority").style("font-size: 20px")
            ticketPriority = ui.toggle(
                {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'})
            ticketDesc = ui.textarea(
                "Enter your issue's description here.").classes('w-10/12 border-2 border-outset border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white')
            ui.button("Submit", on_click=lambda: submitTicket(
            ), color="green", icon="check").classes("py-2 px-4 rounded-full").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    def submitTicket():
        global username
        maxIndexOfTicketNumber = pd.read_sql_query(
            "SELECT MAX(TicketNumber) FROM Tickets", db_tickets)
        indexToUse = maxIndexOfTicketNumber.at[0, 'MAX(TicketNumber)']+1
        print("Inserting into index " + str(indexToUse) +
              " with the following information: ")
        print("Before cleanse: ", ticketTitle.value)
        title = str(ticketTitle.value).replace("'", "''")
        print("After cleanse: ", title)

        print("Before cleanse: ", ticketType.value)
        type = str(ticketType.value).replace("'", "''")
        print("After cleanse: ", type)

        print("Before cleanse: ", ticketDesc.value)
        desc = str(ticketDesc.value).replace("'", "''")
        print("After cleanse: ", desc)

        print("Before cleanse: ", ticketPriority.value)
        priority = str(ticketPriority.value).replace("'", "''")
        print("After cleanse: ", priority)

        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)

        ticketDueDate = ticketTimeStamp + datetime.timedelta(days=3)
        realTicketDueDate = ticketDueDate.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketDueDate)

        # checks which option was chosen by the toggle and changes the number to its corresponding words
        if type == 1:
            type = 'Software'
        else:
            type = 'Hardware'

        # grabs number value from priority option selected and applies it to output so you get a real number instead of some nicegui call
        if priority == 1:
            priority = '1'
        elif priority == 2:
            priority = '2'
        elif priority == 3:
            priority = '3'
        elif priority == 4:
            priority = '4'
        elif priority == 5:
            priority = '5'

        if (len(ticketTitle.value) > 0 and len(ticketDesc.value) > 0):
            cursor = db_tickets.cursor()

            cursor.execute("INSERT INTO Tickets (TicketNumber, Title, Description, Timestamp, Assignee, Status, User, Duedate, Issuetype, Priority) VALUES ('" + str(indexToUse) +
                           "', '" + str(title) + "', '" + str(desc) + "', '" + str(realTicketTimeStamp) + "', 'No Assignee', 'Open', '" + username + "', '" + str(realTicketDueDate) + "', '" + str(type) + "', '" + str(priority) + "')")
            db_tickets.commit()
            cursor.close()

            cursor = db_history.cursor()
            indexOfHistoryNumber = pd.read_sql_query(
                "SELECT MAX(HistoryID) FROM TicketHistory", db_history)
            indexOfHistoryNumber += 1

            print("HISTORY ID IS: " +
                  str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]))
            cursor.execute("INSERT INTO TicketHistory (HistoryID, TicketNumber, Username, Assignee, Description, Timestamp, Updater, Title) VALUES ('" + str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]) +
                           "', '" + str(indexToUse) + "', '" + str(username) + "', 'No Assignee', '" + str(desc) + "', '" + str(realTicketTimeStamp) + "', '" + str(username) + "', '" + str(title) + "')")
            db_history.commit()
            cursor.close()

            ui.open(nonadmin_page)
        else:
            ui.notify("No blank tickets permitted.",
                      type="warning", position="top")

# This lets the user view their tickets list by ticket number and title onl


@ui.page("/nonadmin_ticket_view_list")
def nonadmin_ticket_view_list():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%);
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
        nonadmin_page), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    ui.button("View Ticket Status", on_click=lambda: ui.open(
        nonadmin_view_ticket_status), color="red", icon="arrow_forward").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    global username

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title from Tickets WHERE User = '" + username + "'", db_tickets)

    global queriedTicketNumber
    queriedTicketNumber = [4] * 1

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40').classes(
        'max-h-40 max-w-99').on('cellClicked', lambda event: changeQueriedTicketNumber(int(f'{event.args["value"]}'))).on('cellClicked', lambda event: ui.open(nonadmin_ticket_view_info))
    grid.set_visibility(True)


def changeQueriedTicketNumber(i):
    queriedTicketNumber[0] = i
    # This creates a dropdown for the user to pick from which ticket they would like to view further information on.

# This will show further information. There is also another button to view even more details.


@ui.page("/nonadmin_view_ticket_status")
def nonadmin_view_ticket_status():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%);
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
        nonadmin_ticket_view_list), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    global username

    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber, Status, Timestamp from Tickets WHERE User = '" + username + "'", db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes(
        'max-h-40 max-w-99')
    grid.set_visibility(True)


@ui.page("/nonadmin_ticket_view_info")
def nonadmin_ticket_view_info():
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(31deg, rgba(199,233,191,1) 0%, rgba(236,241,162,1) 30%, rgba(116,245,195,1) 65%, rgba(0,254,255,1) 98%);
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
         #extend-border {{
            background-color: #4f46e5;
            width: 3px;
            height: 50px;
            padding: 0px;
            margin: 0px;
            }} 
        </style>
            """
    ui.html(backgroundHtml)
    global queriedTicketNumber
    print("Showing Ticket " + str(queriedTicketNumber[0]) + ".")
    ticketNumber = queriedTicketNumber[0]
    ticketTitle = pd.read_sql_query(
        "SELECT Title from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketDesc = pd.read_sql_query(
        "SELECT Description from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketAssignee = pd.read_sql_query(
        "SELECT Assignee from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketTimestamp = pd.read_sql_query(
        "SELECT Timestamp from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketStatus = pd.read_sql_query(
        "SELECT Status from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketUsername = pd.read_sql_query(
        "SELECT User from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketDueDate = pd.read_sql_query(
        "SELECT Duedate from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketIssueType = pd.read_sql_query(
        "SELECT Issuetype from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
    ticketPriority = pd.read_sql_query(
        "SELECT Priority from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)
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
        nonadmin_ticket_view_list), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    with ui.row().classes('border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; margin: 20px; background-color: white'):
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket #" + str(ticketNumber))
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Last Updated: " + ticketTimestamp.at[0, "Timestamp"])
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket User: " + ticketUsername.at[0, "User"])
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket Status: " + ticketStatus.at[0, "Status"])
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket Due Date: " + str(ticketDueDate.at[0, "Duedate"]))
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Issue Type: " + str(ticketIssueType.at[0, "Issuetype"]))
        ui.html(f"""<div id='extend-border'></div>""")
        ui.label("Ticket Priority: " + str(ticketPriority.at[0, "Priority"]))
        ui.html(f"""<div id='extend-border'></div>""")

    with ui.column().classes('border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Current Ticket Description: ").tailwind.font_weight(
            'extrabold')
        ui.label(ticketDesc.at[0, "Description"])

    with ui.column().classes('justify-center items-center .p-12').style('text-align: center; padding: 20px; margin: 20px'):
        ui.button("Toggle History", color="red", icon="history", on_click=lambda: createHistory(
        )).style('font-weight: bold; text-align: center').tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    container = ui.row().classes('w-full justify-center')

    def createHistory():
        if len(list(container)) > 0:
            print("clear")
            container.clear()
        else:
            print("fill")
            with container:
                with ui.column().classes('w-max items-center border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style("background-color: white;"):
                    for i in range(0, len(ticketHistoryDesc), 1):
                        ui.label("Ticket Description at " +
                                 ticketHistoryTimestamp.at[i, "Timestamp"] + " by " + ticketHistoryUpdater.at[i, "Updater"] + " with title " + ticketHistoryTitle.at[i, "Title"]).style('text-align: center; padding: 20px').tailwind.font_weight('bold')
                        ui.label(ticketHistoryDesc.at[i, "Description"]).style(
                            'text-align: center; padding: 20px')

    with ui.row().classes('w-full justify-center border-width-thick border-color-indigo'):
        with ui.column().classes('w-full items-center border-width-thick border-color-indigo'):
            ticketDesc = ui.textarea("Update description.").classes('w-10/12 border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style(
                'text-align: center; padding: 20px; margin: 20px; background-color: white')
            ui.button("Submit", on_click=lambda: updateTicket(),
                      color="green", icon="done").style("margin-bottom: 20px").tailwind.animation('bounce').drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
# ______________________________________________________________________
    ticketTitle = ticketTitle.at[0, "Title"]

    def updateTicket():
        global username
        indexToUse = ticketNumber
        print("Updating into index " + str(indexToUse) +
              " with the following information: ")
        print("Before cleanse: ", ticketTitle)
        title = str(ticketTitle).replace("'", "''")
        print("After cleanse: ", title)
        print("Before cleanse: ", ticketDesc.value)
        desc = str(ticketDesc.value).replace("'", "''")
        print("After cleanse: ", desc)
        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")
        print(realTicketTimeStamp)
        if (len(ticketDesc.value) > 0):
            cursor = db_tickets.cursor()
            cursor.execute("UPDATE Tickets SET Title = '" + str(title) + "', Description = '" + str(desc) + "', Assignee = '" + str(ticketAssignee.at[0, "Assignee"]) +
                           "', Status = 'Open', Timestamp = '" + str(realTicketTimeStamp) + "' WHERE TicketNumber = '" + str(ticketNumber) + "'")
            db_tickets.commit()
            cursor.close()

            cursor = db_history.cursor()
            indexOfHistoryNumber = pd.read_sql_query(
                "SELECT MAX(HistoryID) FROM TicketHistory", db_history)
            indexOfHistoryNumber += 1

            print("HISTORY ID IS: " +
                  str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]))
            cursor.execute("INSERT INTO TicketHistory (HistoryID, TicketNumber, Username, Assignee, Description, Timestamp, Updater, Title) VALUES ('" + str(indexOfHistoryNumber.at[0, "MAX(HistoryID)"]) +
                           "', '" + str(ticketNumber) + "', '" + str(username) + "', '" + str(ticketAssignee.at[0, "Assignee"]) + "', '" + str(desc) + "', '" + str(realTicketTimeStamp) + "', '" + str(ticketDueDate) + "', '" + str(username) + "', '" + str(title) + "')")

            db_history.commit()
            cursor.close()

            ui.open(nonadmin_page)
        else:
            ui.notify("No blank description permitted.",
                      type="warning", position="top")
