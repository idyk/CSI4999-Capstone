from nicegui import ui

username = ""


def setUsername(user):
    global username
    username = user
    print("Hello ", username)


def getUsername():
    global username
    print("get", username)
    return username
