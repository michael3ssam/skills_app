import sqlite3
db = sqlite3.connect("new_app.db")
cr = db.cursor()

message = '''
what do you want to do ?
"s" => show all your skills
"a" => add a new skill
"d" => delete a skill
"u" => update skill progress
"q" => quit the app
'''



def commit_and_close():
    db.commit()
    db.close()
    print("changes have been saved successfully")
    print("database is closed successfully")

def commit():
    db.commit()
    print("changes have been saved successfully")


def add_skill():
    skill = input("the skill => ").strip().capitalize()
    cr.execute(f"select name from skills where user_id = {uid} and name = '{skill}'")
    results = cr.fetchone()
    if results == None:
        prog = input("your progress => ")
        cr.execute(f"insert into skills(user_id, name, progress) values({uid}, '{skill}', {prog} )")
    else:
        print("this skill already exists")
        choice = input("do you want to update it? yes/no >> ").strip().lower()
        if choice == "yes":
            prog = input("your progress => ")
            cr.execute(f"update skills set progress = {prog} where user_id = {uid} and name = '{skill}'")


def delete_skill():
    skill = input("the skill => ").strip().capitalize()
    cr.execute(f"select name from skills where user_id = {uid} and name = '{skill}'")
    results = cr.fetchone()
    if results == None:
        print("YOU DON`T HAVE SUCH SKILL YOU IDIOT")
    else:
        cr.execute(f"delete from skills where name = '{skill}' and user_id = {uid} ")

def show_skills():
    cr.execute(f"select name, progress from skills where user_id = {uid}")
    results = cr.fetchall()
    print(f"you have {len(results)} skills already, keep up the good work")
    if len(results) > 0:
        for skill, prog in results:
            print(f"the skill is => {skill}", end=" ")
            print(f"and your progress is => {prog}%")
        # print(results)

def update_skills():
    skill = input("the skill => ").strip().capitalize()
    cr.execute(f"select name from skills where user_id = {uid} and name = '{skill}'")
    results = cr.fetchone()
    if results == None:
        print("you don`t have such skill yet!, just type your progress & You can add it to your skills any way ")
        prog = input("your progress => ")
        cr.execute(f"insert into skills(user_id, name, progress) values({uid}, '{skill}', {prog} )")
    else:
        prog = input("your progress => ")
        cr.execute(f"update skills set progress = {prog} where user_id = {uid} and name = '{skill}'")

def sign_in():
    uname = input("type your username > ").strip().lower()
    upassword = input("type your password > ")
    try:
        cr.execute(f"select user_id from users where name ='{uname}' and password = '{upassword}'")
        global uid
        uid = cr.fetchone()[0]
        #print(uid)
        print(message)
        while True:
            user_input = input("type a command > ").strip().lower()
            commands_list = ["s", "a", "d", "u", "q"]
            if user_input in commands_list:
                if user_input == "s":
                    print("showing skills")
                    show_skills()
                elif user_input == "a":
                    print("adding a skill")
                    add_skill()

                elif user_input == "d":
                    print("deleting a skill")
                    delete_skill()
                elif user_input == "u":
                    print("updating the skills")
                    update_skills()
                else:
                    print("quit the app")
                    break
                if user_input != "s":
                    commit()
            else:
                print(f"{user_input} is not a valid command")
        commit_and_close()
    except:
        # print(er)
        print("please enter valid username and password")
        sign_in()

sign_in()


