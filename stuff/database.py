#from MySQLdb import connect
#from sqlite3 import connect
import pymysql

from stuff.settings import SUBJECTS

class Database:
    def __init__(self):
        self.con = self.con()


    def con(self):
        return pymysql.connect(\
                            host="us-cdbr-east-06.cleardb.net", \
                            user="b0bccc5a1c8a3f", \
                            port=3306, \
                            password="9f921e33", \
                            database="heroku_a531a7133cac0e4")
        

    def check_user_in_db(self, user_id):
        with self.con() as con:
            cur = con.cursor()

            cur.execute(f"SELECT user_id FROM users WHERE user_id='{user_id}'")
            db_user_id = cur.fetchone()
            

            if db_user_id==None:
                cur.execute(f"INSERT INTO users(user_id) VALUES ('{user_id}')")
                self.con = con
                con.commit()
            
            return
            #cur.execute(f"UPDATE users SET username='{user_username}' WHERE user_id='{user_id}'")

            #cur.execute(f"SELECT user_id FROM users")
            #print(cur.fetchall())


    def user_is_admin(self, user_id):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT is_admin FROM users WHERE user_id='{user_id}'")
            is_user_admin = cur.fetchone()[0]

        if is_user_admin=="1":
            return True
        
        return False


    def get_group(self, user_id):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT user_group FROM users WHERE user_id='{user_id}'")
            return cur.fetchone()[0]


    def get_acctype(self, user_id):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT type FROM users WHERE user_id='{user_id}'")
            return cur.fetchone()[0]


    def get_department_by_group(self, group):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT department FROM groups WHERE name_group='{group}'")
            return cur.fetchone()[0]

        
    def get_all_departments_by_course(self, course):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT DISTINCT department FROM groups WHERE course='{course}'")
            return cur.fetchall()


    def get_course_by_group(self, group):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT course FROM groups WHERE name_group='{group}'")
            return cur.fetchone()[0]


    def update_account(self, *argv, user_id, _type):
        if _type=='0':
            arg = 'user_group'

            text = argv[0]
        elif _type=='1':
            arg = 'subjects'

            subjects_list = db.get_user_subjects(user_id).split("-")

            if argv[0] in subjects_list:
                subjects_list.remove(argv[0])
            else:
                subjects_list.append(argv[0])

            while "" in subjects_list:
                subjects_list.remove("")
                
            
            text = "-".join(subjects_list)
            

        with self.con() as con:
            cur = con.cursor()

            cur.execute(f"UPDATE users SET type='{_type}', {arg}='{(text)}' WHERE user_id='{user_id}'")
            self.con = con
            return con.commit()


    def get_all_groups_by_dep_and_cour(self, department, course):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT name_group FROM groups WHERE course='{course}' AND department='{department}'")
            return cur.fetchall()


    def is_created_account(self, user_id):
        with self.con as con:
            cur = con.cursor()
            cur.execute(f"SELECT type FROM groups WHERE user_id='{user_id}'")
            type = cur.fetchone()[0]

        if type in ['0', '1']:
            return True

        return False


    def get_all_user_id(self):
        with self.con as con:
            cur = con.cursor()
            cur.execute("SELECT user_id FROM users")
            return cur.fetchall()


    def delete_user(self, user_id):
        with self.con() as con:
            cur = con.cursor()

            cur.execute(f"DELETE FROM users WHERE user_id='{user_id}'")
            self.con = con
            return con.commit()


    def set_admin(self, user_id):
        with self.con() as con:
            cur = con.cursor()

            cur.execute(f"UPDATE users SET is_admin=1 WHERE user_id='{user_id}'")
            self.con = con
            return con.commit()


    def change_acctype(self, user_id, type):
        with self.con() as con:
            cur = con.cursor()

            cur.execute(f"UPDATE users SET is_admin={type} WHERE user_id='{user_id}'")
            self.con = con
            return con.commit()


    def get_user_subjects(self, user_id):
        with self.con as con:
            cur = con.cursor()
            
            cur.execute(f"SELECT subjects FROM users WHERE user_id='{user_id}'")
            return cur.fetchone()[0]


    def get_all_subjects(self):
        return SUBJECTS

    

#db = Database("C:/Users/nazar/Desktop/saq/Python/uwu/nubip_bot/database/nubip.db")
db = Database()