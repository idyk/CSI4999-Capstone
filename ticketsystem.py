from nicegui import ui
import sqlite3
import pandas as pd
import datetime
from nicegui import Tailwind, ui


db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')

# The page that the user will see on first launch.


@ui.page('/login_page')
def login_page():
    # Since local files get encrypted on launch, you can get around it by getting the source from ui.image and then using it in HTML :)
    # bgSource = ui.image("./images/test.gif").style("display: none;").source
    # backgroundHtml = f"""
    #     <style>
    #         body {{
    #             background-image: url("{bgSource}");
    #             background-repeat: no-repeat;
    #             background-size: cover;
    #         }}
    #     </style>
    #         """
    backgroundHtml = f""" 
        <style> 
            body {{
                background: linear-gradient(-45deg, #6495ED, #00FFFF);
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

    with ui.row().classes('w-full justify-center'):
        with ui.column().classes('w-full items-center'):
            # ui.query('body').style(
            #     'background-image: linear-gradient(to right, #6495ED, #00FFFF); font-family: Sans-serif')
            ui.label("Welcome to TICKSTER").style(
                'color: white; font-size: 40px; font-weight: bold; text-shadow: 2px 2px 4px black; -webkit-text-stroke-width: 2px; -webkit-text-stroke-color: black;')
            ui.label("Please login with your credentials to access the system.").style(
                'color: white; font-weight: bold; font-size: 30px; -webkit-text-stroke-width: 1px; text-shadow: 2px 2px 4px black; -webkit-text-stroke-color: black;')
            with ui.column().classes('w-6/12 border-4 border-outset border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
                username = ui.input(label="Username").classes(
                    'border-2 border-solid border-indigo-600 rounded-lg ').style("width: 30%")
                password = ui.input(label="Password", password=True,
                                    ).classes('border-2 border-inset border-indigo-600 .p12 rounded-lg ').style("width: 30%")

        ui.button("Sign in", on_click=lambda: attemptLogin(
        ), color="green", icon="how_to_reg").classes("py-2 px-4 rounded-full ").tailwind.drop_shadow('lg').animation('bounce').box_shadow('inner').box_shadow_color('black').gradient_color_stops('from-10%').justify_content('center')

    # This checks the username and password against the login database for validation. It will also check if the user is elevated or not to
    # direct them to the correct set of pages.

    def attemptLogin():
        # print(bgSource)
        usernameSqlQueryCheck = pd.read_sql_query(
            "SELECT Username FROM Logins WHERE Username = '" + username.value + "'", db_login)
        passwordSqlQueryCheck = pd.read_sql_query(
            "SELECT Password FROM Logins WHERE Password = '" + password.value + "'", db_login)
        elevatedSqlQueryCheck = pd.read_sql_query(
            "SELECT Elevated FROM Logins WHERE Username = '" + username.value + "'", db_login)

        try:
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
        except:
            ui.notify("Invalid login.", type="negative", position="top")


# This lets us set the username. Not sure if it's even needed but yeah...
def setUsername(user):
    print("setting global username to: " + user)
    global username
    username = user

# First nonadmin page. Has create ticket and view ticket buttons.


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

    ui.button("Logout", on_click=lambda: ui.open(
        login_page), icon="logout", color="red").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
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
        nonadmin_page), color="red", icon="arrow_back")
    ui.button("View Ticket Status", on_click=lambda: ui.open(
        nonadmin_view_ticket_status), color="red", icon="arrow_forward")

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
        nonadmin_ticket_view_list), color="red", icon="arrow_back")

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

    with ui.row().classes('border-2 border-indigo-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Ticket #" + str(ticketNumber))
        ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
        ui.label("Last Updated: " + ticketTimestamp.at[0, "Timestamp"])
        ui.label("Ticket User: " + ticketUsername.at[0, "User"])
        ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
        ui.label("Ticket Status: " + ticketStatus.at[0, "Status"])
        ui.label("Ticket Due Date: " + str(ticketDueDate.at[0, "Duedate"]))
        ui.label("Issue Type: " + str(ticketIssueType.at[0, "Issuetype"]))
        ui.label("Ticket Priority: " + str(ticketPriority.at[0, "Priority"]))

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

# ADMIN VIEW SECTION!!!!!!!!!


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
        login_page), icon="logout", color="red").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    with ui.row().classes('w-full justify-center border-width-thick border-color-red'):
        with ui.column().classes('w-full items-center'):
            ui.label("Hello " + str(username) +
                     "!").style("font-size: 40px; font-weight: bold").tailwind.animation('bounce')
            ui.label("Please select from the options below.").style(
                "font-size: 25px;")
            ui.button("View Created Tickets", on_click=lambda: ui.open(
                admin_ticket_view_list), color="orange", icon="search").classes("py-2 px-4 rounded-full").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
            ui.button("Create A User", on_click=lambda: ui.open(
                admin_create_user), color="pink", icon="add").classes("py-2 px-4 rounded-full").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')


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
        admin_page), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    with ui.row().classes('w-2/3 border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin-left: auto; margin-right: auto; background-color: white'):
        with ui.column().classes('w-full items-center'):
            newUsername = ui.input(
                "Create username.").classes('w-50 items-center').style("text-align: center; font-weight: bold")
            newPassword = ui.input(
                "Create password.").classes('w-50 items-center').style("text-align: center; font-weight: bold")
            ui.label("Elevated?")
            elevationStatus = ui.select(options=["False", "True"])
            ui.button("Create User", on_click=lambda: generateUser(
                newUsername.value, newPassword.value, elevationStatus.value), color="green", icon="add_circle").tailwind.animation('bounce').drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

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
    ui.button("Go back", on_click=lambda: ui.open(admin_page), color="red",
              icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')
    ui.button("Number of Tickets per User", on_click=lambda: ui.open(
        admin_created_tickets_by_user), color="red", icon="arrow_forward")

    global username

    print("Username getting pulled is " + username)
    df_tickets = pd.read_sql_query(
        "SELECT TicketNumber,Title,User from Tickets", db_tickets)

    global queriedTicketNumber
    queriedTicketNumber = [4] * 1

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40').classes(
        'max-h-40 max-w-99').on('cellClicked', lambda event: changeQueriedTicketNumber(int(f'{event.args["value"]}'))).on('cellClicked', lambda event: ui.open(admin_ticket_view_info))
    grid.set_visibility(True)


@ui.page("/admin_created_tickets_by_user")
def admin_created_tickets_by_user():
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
        admin_ticket_view_list), color="red", icon="arrow_back")

    global username

    table_data = """
        SELECT User AS Username, 
        COUNT(User) AS TotalTicketsCreated,
        SUM(CASE WHEN Status='Open' THEN 1 ELSE 0 END) AS NumberOfOpenTickets,
        SUM(CASE WHEN Status='Resolved' THEN 1 ELSE 0 END) AS NumberOfResolvedTickets,
        SUM(CASE WHEN Status='On Hold' THEN 1 ELSE 0 END) AS NumberOfOnHoldTickets
        FROM Tickets
        WHERE User != 'admin'
        GROUP BY User
        """

    df_tickets = pd.read_sql_query(table_data, db_tickets)

    grid = ui.aggrid.from_pandas(df_tickets).classes('max-h-40 max-w-99')
    grid.set_visibility(True)


def changeQueriedTicketNumber(i):
    queriedTicketNumber[0] = i


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

    print("Showing Ticket " + str(queriedTicketNumber[0]) + ".")

    ticketNumber = queriedTicketNumber[0]

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

    ticketDueDate = pd.read_sql_query(
        "SELECT Duedate from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

    ticketIssueType = pd.read_sql_query(
        "SELECT IssueType from Tickets WHERE TicketNumber = '" + str(ticketNumber) + "'", db_tickets)

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
        admin_ticket_view_list), color="red", icon="arrow_back").tailwind.drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

    with ui.row().classes('border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Ticket #" + str(ticketNumber))
        ui.label("Ticket Title: " + ticketTitle.at[0, "Title"])
        ui.label("Last Updated: " + ticketTimestamp.at[0, "Timestamp"])
        ui.label("Ticket User: " + ticketUsername.at[0, "User"])
        ui.label("Ticket Assignee: " + ticketAssignee.at[0, "Assignee"])
        ui.label("Ticket Status: " + ticketStatus.at[0, "Status"])
        ui.label("Ticket Due Date: " + str(ticketDueDate.at[0, "Duedate"]))
        ui.label("Issue Type: " + str(ticketIssueType.at[0, "Issuetype"]))
        ui.label("Ticket Priority: " + str(ticketPriority.at[0, "Priority"]))

    with ui.column().classes('border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style('text-align: center; padding: 20px; margin: 20px; background-color: white'):
        ui.label("Current Ticket Description: ").tailwind.font_weight('bold')
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
                with ui.column().classes('w-max items-center border-2 border-red-600 justify-center items-center .p-12 rounded-lg').style("background-color: white;"):
                    for i in range(0, len(ticketHistoryDesc), 1):
                        ui.label("Ticket Description at " +
                                 ticketHistoryTimestamp.at[i, "Timestamp"] + " by " + ticketHistoryUpdater.at[i, "Updater"] + " with title " + ticketHistoryTitle.at[i, "Title"]).style('text-align: center; padding: 20px').tailwind.font_weight('bold')
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
        ui.label("Change Priority").style("font-size: 20px")
        ticketPriority = ui.toggle({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'})
        ticketTitle = ui.textarea(
            "Update title").classes('w-full')
        ticketDesc = ui.textarea("Update description.").classes('w-full')
        ui.button("Submit", on_click=lambda: updateTicket(),
                  color="green", icon="done").style("margin-bottom: 20px").tailwind.animation('bounce').drop_shadow('lg').box_shadow('inner').box_shadow_color('black')

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

        print("Before cleanse: ", ticketPriority.value)
        priority = str(ticketPriority.value).replace("'", "''")
        print("After cleanse: ", priority)

        ticketTimeStamp = datetime.datetime.now()
        realTicketTimeStamp = ticketTimeStamp.strftime(
            "%b %d %Y") + " at " + ticketTimeStamp.strftime("%H") + ":" + ticketTimeStamp.strftime("%M")

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

        print(realTicketTimeStamp)
        if (len(ticketTitle.value) > 0 and len(ticketDesc.value) > 0):
            cursor = db_tickets.cursor()
            cursor.execute("UPDATE Tickets SET Title = '" + str(title) + "', Description = '" + str(desc) + "', Assignee = '" + str(selectedAssignee.value) +
                           "', Status = '" + str(selectedStatus.value) + "', Timestamp = '" + str(realTicketTimeStamp) + "', Priority = '" + str(priority) + "' WHERE TicketNumber = '" + str(ticketNumber) + "'")
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


login_page()
ui.run(title="TICKSTER - IT Ticketing System", favicon="✔")
