from nicegui import ui
import sqlite3
import pandas as pd

db_con = sqlite3.connect(r'C:\Users\dykas\Desktop\testprojectpy\test.db')
df = pd.read_sql_query("SELECT * from Tickets", db_con)

@ui.page('/tables_page')
def tables_page():
    grid = ui.aggrid.from_pandas(df).classes('max-h-40')
    ui.button('Toggle Grid', on_click=lambda: toggleGrid())

    def toggleGrid():
      if(grid.visible):
        print("grid is visible, hiding")
        grid.set_visibility(False)
      else:
        print("grid isn't visible, showing")
        grid.set_visibility(True)


def login_page():
    ui.link('Login', tables_page)

login_page()

ui.run()