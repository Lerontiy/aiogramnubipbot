#from MySQLdb import connect
import asyncio
import sqlite3
import aiomysql

from stuff.settings import SUBJECTS

class Database:
    def __init__(self):
        self.con = self.sql_connect()
        self.loop = asyncio.get_event_loop()


    async def mysql_connect(self):
        return await aiomysql.connect(\
                            host="eu-cdbr-west-03.cleardb.net", \
                            user="bc5c7f07563fec", \
                            port=3306, \
                            password="765381bc", \
                            db="heroku_aa604352b17cb1e", \
                            loop=self.loop
                            )


    def sql_connect(self):
        return sqlite3.connect('stuff/nubip.db')
    

    def update_sql(self, request):
        with self.sql_connect() as con:
            cur = con.cursor()
            cur.execute(request)
            con.commit()
            self.con = con
        asyncio.run(self.update_mysql(request))
        return
    

    async def update_mysql(self, request):
        async with await self.mysql_connect() as con:
            async with await con.cursor() as cur:
                await cur.execute(request)
            await con.commit()
        return


    async def recreate_sql(self):
        async with await self.mysql_connect() as con:
            async with await con.cursor() as cur:
                await cur.execute("SELECT * FROM users")
                all = await cur.fetchall()

        with self.sql_connect() as sql_con:
            sql_cur = sql_con.cursor()
            sql_cur.execute("DELETE FROM users")

            for el in all:
                #print(el)
                sql_cur.execute("INSERT INTO users VALUES('{}', '{}', '{}', '{}', '{}')".format(*el))

            #self.con.execute("DELETE FROM groups")
            #cur.execute("SELECT * FROM groups")
            #all = cur.fetchall()
            #for el in all:
            #    self.con.execute(f"INSERT INTO groups VALUES(?, ?, ?)", el)

            del all

            sql_con.commit()

        return await asyncio.sleep(0)


    async def mysql_request(self, cur, el):
        await cur.execute("INSERT INTO users VALUES('{}', '{}', '{}', '{}', '{}')".format(*el))
        return 

    async def recreate_mysql(self):
        with self.sql_connect() as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM users")
            all = cur.fetchall()

        async with await self.mysql_connect() as mysql_con:
            async with await mysql_con.cursor() as mysql_cur:
                await mysql_cur.execute("DELETE FROM users")


                n_all = []
                u_id = []
                for el in all:
                    if el[0] not in u_id:
                        u_id.append(el[0])
                        n_all.append(el)
                all = n_all
                del n_all, u_id


                for el in all:
                    print(el)
                    await self.mysql_request(mysql_cur, el)

                    #task = asyncio.create_task(self.mysql_request(mysql_cur, el))
                    #tasks.append(task)

                #print(tasks)
                #start_time = time.time()
                #await asyncio.gather(*tasks)
                #for i in tasks:
                #    await i
                #print(time.time() - start_time)

                await mysql_con.commit()

                del all

        return


    def check_user_in_db(self, user_id):
        with self.con as con:
            cur = con.cursor()

            cur.execute(f"SELECT user_id FROM users WHERE user_id='{user_id}'")
            db_user_id = cur.fetchone()
            

        if db_user_id==None:
            #with self.sql_connect() as con:
                #cur = con.cursor()
                #cur.execute(f"INSERT INTO users(user_id) VALUES ('{user_id}')")
                #con.commit()

            self.update_sql(f"INSERT INTO users(user_id) VALUES ('{user_id}')")
        return


    def update_account(self, addition, user_id, _type):
        if _type=='0':
            arg = 'user_group'

            text = addition
        elif _type=='1':
            arg = 'subjects'

            subjects_list = db.get_user_subjects(user_id).split("-")

            if addition in subjects_list:
                subjects_list.remove(addition)
            else:
                subjects_list.append(addition)

            while "" in subjects_list:
                subjects_list.remove("")

            # згідно абетки
            subjects_list_by_alphabet = []
            for id, name in SUBJECTS.items():
                if id in subjects_list:
                    subjects_list_by_alphabet.append((id, name))

            subjects_list = dict(sorted(subjects_list_by_alphabet, key=lambda x: x[1], reverse=False))
            subjects_list = subjects_list.keys()

            text = "-".join(subjects_list)
            
            del subjects_list_by_alphabet

        #with self.sql_connect() as con:
        #    import time
        #    start_time = time.time()
        #    cur = con.cursor()
        #    cur.execute(f"UPDATE users SET type='{_type}', {arg}='{(text)}' WHERE user_id='{user_id}'")
        #    con.commit()

            #print(time.time() - start_time)
            #start_time = time.time()

        self.update_sql(f"UPDATE users SET type='{_type}', {arg}='{(text)}' WHERE user_id='{user_id}'")

            #print(time.time() - start_time)
        
        return
    

    def delete_user(self, user_id):
        #with self.sql_connect() as con:
        #    cur = con.cursor()
        #    cur.execute(f"DELETE FROM users WHERE user_id='{user_id}'")
        #    con.commit()

        self.update_sql(f"DELETE FROM users WHERE user_id='{user_id}'")
        return


    def set_admin(self, user_id):
        #with self.sql_connect() as con:
        #    cur = con.cursor()
        #    cur.execute(f"UPDATE users SET is_admin=1 WHERE user_id='{user_id}'")
        #    con.commit()

        self.update_sql(f"UPDATE users SET is_admin=1 WHERE user_id='{user_id}'")

        return


    def change_acctype(self, user_id, type):
        #with self.sql_connect() as con:
        #    cur = con.cursor()
        #    cur.execute(f"UPDATE users SET is_admin={type} WHERE user_id='{user_id}'")
        #    con.commit()

        self.update_sql(f"UPDATE users SET is_admin={type} WHERE user_id='{user_id}'")
        return
    
    # ----------------------
    
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
        

    def get_user_subjects(self, user_id):
        with self.con as con:
            cur = con.cursor()
            
            cur.execute(f"SELECT subjects FROM users WHERE user_id='{user_id}'")
            return cur.fetchone()[0]


    def get_all_subjects(self):
        return SUBJECTS

    

#db = Database("C:/Users/nazar/Desktop/saq/Python/uwu/nubip_bot/database/nubip.db")
db = Database()