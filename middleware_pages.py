# from admin import open_admin
from nicegui import ui


def start_page():
    from login import startup
    startup()


def open_login_page():
    from login import open_login
    open_login()


def open_nonadmin_page():
    from nonadmin import open_nonadmin
    print("opening nonadmin")
    open_nonadmin()


def open_admin_page():
    from admin import open_admin
    print("opening admin")
    open_admin()
