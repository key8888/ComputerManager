from datetime import date

def make_password():
    today:str = date.today().strftime("%m%d")
    password:str = str(int(today) * 2 - 2)
    if len(password) < 4:
        password = "0" * (4 - len(password)) + password
    return password