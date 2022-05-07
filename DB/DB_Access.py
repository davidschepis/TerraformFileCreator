import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="rg_manager"
)

class DB:
    def login(username, password):
        username = username.replace(" ", "")
        password = password.replace(" ", "")
        myc = mydb.cursor()
        myc.execute(f"select username, id, authorized_by from users where username='{username}' and u_password='{password}'")
        result = myc.fetchall()
        if (len(result) < 1):
            return False
        return result[0]
    
    def signup(username, password, authorized_by):
        try:
            username = username.replace(" ", "")
            password = password.replace(" ", "")
            myc = mydb.cursor()
            myc.execute(f"insert into users (username, u_password, authorized_by) values ('{username}', '{password}', '{authorized_by}')")
            mydb.commit()
            return True
        except mysql.connector.Error as e:
            return False
    
    def list_users():
        myc = mydb.cursor()
        myc.execute("select username, id, authorized_by from users")
        result = myc.fetchall()
        return result