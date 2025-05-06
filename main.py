import os, json, random, datetime, time

db = {}
sv = {}
settings = {}
mode = 0
random.seed()
os.system("")

def ret_time(i):
    
    s = i
    p = 0
    
    while(s // 60):
        p += 1
        s = s // 60

    arr = []
    if(p > 2): arr.append(i%(60**3))
    p = min(p, 2)
    
    for w in range(p, -1, -1):
        if not w: arr.append(i%60)
        else: arr.append((i % 60**(w+1))//(60**w))
    
    return arr

DEFAULT = {"user": {"OPENFILE":True, "AUTOSAVE":False}, "db": {"WEB": "", "CDIR": os.getcwd(), "DBPATH": "db.json"}}
INDENT = lambda n: "\t"*n
BR = lambda n: "\n"*n
SPACE = lambda n: " "*n 
COLOR = lambda t, r, g, b: f"\x1b[38;2;{r};{g};{b}m" + t + "\x1b[0m"
QST = lambda q, f: {"qst": q, "file": f, "mtag": "ad hoc", "tags": []}
is_saved = True

def open_problem(pcode):

    global db

    print("")

    try: print(pcode + ": " + db["problems"][pcode]["qst"] + BR(1))
    except KeyError: 
        print("Problem code not found. Reload database with (open) or add entry with (set). See (help) for instructions." + BR(1))
        return
    
    handle_pbrequest(pcode)

def handle_pbrequest(pcode):

    s = input("What would you like to do?" + BR(1) + 
              "(:t): start timer".ljust(30) + 
              "(:f): open editorial".ljust(30) + 
              "(:s): mark as solved".ljust(30) + 
              "(:h): get problem tags (hints)" + BR(1) +
              "(:c): close")
    print("")

    match s.lower():

        case "(:t)":

            t0 = time.perf_counter()
            input("Timer started. Press enter to stop.")
            res = ret_time(time.perf_counter() - t0)
            print(" ".join([str(int(res[i])) + ["d", "h", "min", "s"][i + 4 - len(res)] for i in range(len(res))]))
            handle_pbrequest(pcode)
        
        case "(:h)": 
            print("tags: " + ", ".join(db["problems"][pcode]["tags"]))

        case "(:s)": sv[pcode]["solved"] = True

        case "(:f)":

            try: 
                f = open(settings["CDIR"] + "/philoforces-db/question_pool/" + db["problems"][pcode]["file"], "x")
                f.close()
            except: 
                pass

            os.startfile(settings["CDIR"] + "/philoforces-db/question_pool/" + db["problems"][pcode]["file"])

        case "(:c)": return

def init_database():
    
    global db

    try: 

        with open(settings["CDIR"] + "/philoforces-db/" + settings["DBPATH"], "r") as f:
            db = json.load(f)

        for k in db["problems"]:

            if(not sv.__contains__(k)):

                sv[k] = {}
                sv[k]["Solved"] = False

    except: print("could not find JSON database." + " " 
                + f"Make sure {settings['DBPATH']} is in current directory ({settings['CDIR']})" + " "
                + "or change current directory / database file path with" + " "
                + "(settings -change) CDIR [dir] / (settings -change) DBPATH [dir]" + " " +
                "and reopen database with (open)"
                )

def save_database():

    global db

    try:
        with open(settings["CDIR"] + "/philoforces-db/" + settings["DBPATH"], "w") as f:
            json.dump(db, f)
            return True
    except: 

        print("Error saving changes. Could not open JSON database.")
        return False

def load_settings():

    global settings, DEFAULT

    try: 
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except: pass

    for k in DEFAULT: 
        if not settings.__contains__(k):  settings[k] = DEFAULT[k]

def save_settings():

    global settings

    try: 
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    except: 
        print("Error saving settings.")

def load_save():

    global sv

    try: 
        with open("save.json", "r") as f:
            sv = json.load(f)
    except: 
        print("Error loading save.")

def save2():

    try: 
        with open("save.json", "w") as f:
            json.dump(sv, f)
    except: 
        print("Error saving progress.")

def help_common():

    print(BR(1) + "Welcome to philoforces terminal edition.\n" +
                  "Commands are used in the following format: (cmd [-options]) [*args -> arg1 : arg2 : ...]:" + BR(1))

    print("(exit): leave." + BR(1))

    print("(mode): changes mode from user (user) to database editor (database)." + BR(1))

    print("(settings [-option]): change program settings" + BR(1) + INDENT(1) + 
                "-print [*args]: prints queried settings; leave empty to get all" + BR(1) + INDENT(1) + 
                "-change [setting] [arg]: changes setting to passed argument" + BR(1)
        )

    print("(clear): clears terminal of all previous queries" + BR(1))

    print("(open): opens question database" + BR(1) + INDENT(1) + 
                  "-online: queries file from git repo" + BR(1))

    print("(get) [pbcode]: opens problem associated to passed problem code" + BR(1))

    print("(list): lists all problems available in current database" + BR(1))

    # TODO: Implement random
    print("(toggle) [pbcode]: toggles status of problem associated to problem code to solved/unsolved" + BR(1))

    print("(random [-option]) [*args]: returns random question" + BR(1) + INDENT(1) + 
                    "-tags [*args]: returns random question with any one of the tags passed as argument" + BR(1) + INDENT(1) + 
                    "-philosophers [*args]: returns random question with any one of the passed philosophers" + BR(1)
            )

def handle_common(cmd, args):

    match cmd[0].lower():

        case "settings":

            if cmd[1] == "-print": 
            
                print("")

                if args:
                    for k in args:     
                        try: 
                            print(k.ljust(10) + str(settings["user"][k]))
                        except KeyError: pass

                else:
                    print("User settings:" + BR(1))
                    for k in settings["user"]: print(k.ljust(10) + str(settings[k]))

            elif cmd[1] == "-change": settings[args[0]] = args[1]

            if(not mode): print("")

        case "open": 
            
            if(len(cmd) > 1):
                if(cmd[1] == "-online"): 
                    os.system("git clone https://github.com/Superomego-cloud/philoforces-db.git")
            init_database()

        case "get": open_problem(args[0])

        case "list":

            if not args: args = db["tags"].keys() 

            for t in args:

                pbarr = db["tags"][t]

                if(len(pbarr) == 1): continue
                
                x, y, z = ((0, 255, 0) if pbarr[0] == len(pbarr) - 1 else 
                        ((255, 255, 0) if pbarr[0] else (255, 0, 0)))

                print(COLOR(f"{t}: [{pbarr[0]}/{len(pbarr) - 1}]", x, y, z) + BR(1))

                for p in pbarr[1:]:
                    
                    x, y, z = ((0, 255, 0) if db["problems"][p]["solved"] else (255, 0, 0))
                    print(COLOR(p + ": " + db["problems"][p]["qst"], x, y, z))
                
                print("")

        case "toggle":

            try:
                sv[args[0]]["Solved"] = not sv[args[0]]["Solved"]
            except KeyError:
                print("Problem not found. Try again with correct problem name.")

        case "clear": 
            print("\x1b[2J\x1b[HPHILOFORCES TERMINAL EDITION V0")
            print("Made by yours truly. Print (help) for instructions." + BR(1))


def user_mode(cmd, args):

    match cmd[0].lower():

        case "help": help_common() 
        case _:

            handle_common(cmd, args)


def db_mode(cmd, args):

    global is_saved

    match cmd[0].lower():

        case "help":
            
            help_common()

            print("===== ===== =====" + " ELEVATED COMMANDS " + "===== ===== =====" + BR(1))

            print("(set) [pbcode] : [question] : [file] : *[tags]: changes text entry associated to problem code to new file;" + " " 
                + "if problem code doesn't exist, it will be added to the database" + BR(1))

            print("(delete) [pbcode]: deletes entry associated to passed problem code" + BR(1))

            print("(tag) [pbcode] [*args]: adds tags to problem passed as argument." + BR(1) + INDENT(1) +
                    "-main: sets first argument as main tag" + BR(1) + INDENT(1) +
                    "-delete: removes all tags" + BR(1))

            print("(save): saves changes done to current database. Exit without saving to get unedited version" + BR(1) + INDENT(1)
                  + "-online: queries change to online repo via git; Only allowed for elevated git users. Make sure you are logged in." + BR(1))

        case "settings":

            handle_common()

            if cmd[1] == "-print": 

                if args:
                    for k in args:     
                        try: 
                            print(k.ljust(10) + str(settings["db"][k]))
                        except KeyError: pass

                else: 
                    print(BR(1) + "Database settings:" + BR(1))
                    for k in settings["db"]: print(k.ljust(10) + str(settings[k]))
                
            print("")

        case "save": 

            if(len(cmd) > 1):
                if(cmd[1] == "-online"):
                
                    c = os.getcwd()
                    os.chdir(settings["CDIR"] + "/philoforces-db")
                    os.system("git add .")
                    os.system(f'git commit -m "Remote change done at {datetime.datetime.now().ctime()}"')
                    os.system("git branch -M main")
                    os.system("git remote rm philoforces-db")
                    os.system("git remote add philoforces-db https://github.com/Superomego-cloud/philoforces-db.git")
                    os.system(f"git push -u philoforces-db main")
                    os.chdir(c)

            save_database()
            is_saved = True

        case "set": 

            db["problems"][args[0]] = QST(args[1], args[2])
            is_saved = False

        case "tag":

            if(len(cmd) == 1):
                for t in args[1:]: 
                    if(t not in db["problems"][args[0]]["tags"]): db["problems"][args[0]]["tags"].push(t)
            else:
                
                db["problems"][args[0]]["mtag"] = args[1]

                if(len(cmd) > 2):
                    for t in args[2:]: 
                        if(t not in db["problems"][args[0]]["tags"]): db["problems"][args[0]]["tags"].push(t)    

        case "delete":

            del db["problems"][args[0]]
            is_saved = False

        case _: user_mode(cmd, args)

print("\x1b[2J\x1b[HPHILOFORCES TERMINAL EDITION V0")
print("Made by yours truly. Print (help) for instructions." + BR(1))
load_settings()
load_save()
init_database()

while True:

    ip = (input(">>> ") + " ").split(") ")
    cmd = [w.strip() for w in ((ip[0])[1:]).split(" ")]
    args = []

    if(ip[1]): args = [w.strip() for w in ip[1].split(" : ")]

    try:

        match cmd[0].lower():

            case "exit": 

                if(settings["AUTOSAVE"]): save_database()
                
                elif(not is_saved): 

                    ip = input("It seems you have some unsaved changes. Would you like to save them? [Y/N]: ")
                    ip = ip.strip()
                    if(ip == "Y"): save_database()
                
                save_settings()
                save2()
                exit()


            case "mode":
                if(args[0] == "user"): mode = 0
                elif(args[0] == "database"): mode = 1

            case _:

                if(mode): db_mode(cmd, args)
                else: user_mode(cmd, args)


    except IndexError:
        print("Incorrect amount of arguments.")