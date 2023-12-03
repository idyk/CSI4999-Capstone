from nicegui import ui
import sqlite3
import pandas as pd
import datetime
from middleware_pages import open_nonadmin_page
from middleware_pages import open_admin_page

from middleware_variables import setUsername

db_tickets = sqlite3.connect(r'.\tickets.db')
db_login = sqlite3.connect(r'.\login.db')
db_history = sqlite3.connect(r'.\history.db')


def startup():
    login_page()


def open_login():
    print("open")
    ui.open(login_page)


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
                        open_nonadmin_page()
                    else:
                        open_admin_page()
        except:
            ui.notify("Invalid login.", type="negative", position="top")
