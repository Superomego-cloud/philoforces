import os, json, random, datetime, time, copy

db = {}
bc = {}
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

DEFAULT = {"user": {"OPENFILE":True}, "db": {"AUTOSAVE":False, "WEB": "", "CDIR": os.getcwd(), "DBPATH": "db.json"}}
INDENT = lambda n: "\t"*n
BR = lambda n: "\n"*n
SPACE = lambda n: " "*n 
COLOR = lambda t, r, g, b: f"\x1b[38;2;{r};{g};{b}m" + t + "\x1b[0m"
QST = lambda q, f: {"qst": q, "file": f, "mtag": "Ad hoc", "tags": []}
LINEUP = lambda p: f"\x1b[{p}A"
CLEARSCR = "\x1b[2J\x1b[H"
CLEARSCREEN =  CLEARSCR + "PHILOFORCES TERMINAL EDITION V0" + BR(1) + "Made by yours truly. Print (help) for instructions." + BR(2)
CLEARLINE = "\x1b[2K\r"
is_saved = True

def open_problem(pcode):

    global db

    try: 
        print(CLEARSCR + pcode + ": " + db["problems"][pcode]["qst"] + BR(1))
    except KeyError: 
        print("Problem code not found. Reload database with (open) or add entry with (set). See (help) for instructions.")
        return
    
    handle_pbrequest(pcode)

def create_problem(pbcode, qst, file, tags):

    pb = QST(qst, file)
    if tags:
        pb["mtag"] = tags[0]
        for t in tags[1:]:
            pb["tags"].append(t)
    else: 
        pb["mtag"] = "Ad hoc" 
        
    if pb["mtag"] not in db["tags"]:
        db["tags"][pb["mtag"]] = [0]

    db["problems"][pbcode] = pb
    db["tags"][pb["mtag"]].append(pbcode)
    sv[pbcode] = {"solved": False} 
    

def delete_problem(pbcode):
    
    db["tags"][db["problems"][pbcode]["mtag"]].remove(pbcode)
    del db["problems"][pbcode]
    del sv[pbcode]


def handle_pbrequest(pcode):

    print("What would you like to do?" + BR(1) + 
          "(:t): start timer".ljust(30) + 
          "(:f): open editorial".ljust(30) + 
          "(:s): mark as solved".ljust(30) + 
          "(:h): get problem tags (hints)" + BR(1) +
          "(:c): close" + BR(1))

    while True:

        s = input("")

        match s.lower():

            case "(:t)":

                t0 = time.perf_counter()
                input("\x1b[1ATimer started. Press enter to stop.")
                res = ret_time(time.perf_counter() - t0)
                print("\x1b[1A\x1b[2K\r", end="") 

                print("Attempt over. Time: " + 
                      "".join(
                          [str(int(res[i])) + ["d", "h", "min", "s"][i + 4 - len(res)] 
                           for i in range(len(res))]
                        )
                    )
            
            case "(:h)":

                n = "none"

                if(not db["problems"][pcode]["tags"]):
                    if (db["problems"][pcode]["mtag"] != "Ad hoc"): n = db["problems"][pcode]["mtag"]
                else:
                    n = db["problems"][pcode]["mtag"] + ", " + ", ".join(db["problems"][pcode]["tags"])

                print(LINEUP(1) + "tags: " + n)

            case "(:s)": 
                sv[pcode]["solved"] = True
                print(LINEUP(1) + "Problem marked solved.")

            case "(:f)":

                try: 
                    f = open(settings["db"]["CDIR"] + "/philoforces-db/question_pool/" + db["problems"][pcode]["file"], "x")
                    f.close()
                except: 
                    pass
                
                os.startfile(settings["db"]["CDIR"] + "/philoforces-db/question_pool/" + db["problems"][pcode]["file"])
                print(LINEUP(1) + "Editorial opened.")

            case "(:c)":
                print(CLEARSCREEN, end="") 
                return

            case _:
                print(LINEUP(1) + "Invalid command.")

def init_database():
    
    global db

    try: 
        with open(settings["db"]["CDIR"] + "/philoforces-db/" + settings["db"]["DBPATH"], "r") as f:
            db = json.load(f)
    except: 
        print("could not find JSON database." + " " 
                + f"Make sure {settings["db"]['DBPATH']} is in current directory ({settings["db"]['CDIR']})" + " "
                + "or change current directory / database file path with" + " "
                + "(settings -change) CDIR [dir] / (settings -change) DBPATH [dir]" + " " +
                "and reopen database with (open)"
                )
        return

    for k in db["problems"]:

            if(not sv.__contains__(k)):

                sv[k] = {}
                sv[k]["solved"] = False

    if(not db["tags"].__contains__("Ad hoc")):
        db["tags"]["Ad hoc"] = [0]

    for k in db["tags"]:

        db["tags"][k][0] = 0

        for p in db["tags"][k][1:]:
            if(sv[p]["solved"]): db["tags"][k][0] += 1

def save_database():

    global db
    k = list(db["tags"].keys())

    for t in k:
        if (len(db["tags"][t]) == 1) and (t != "Ad hoc"): del db["tags"][t]

    try:
        with open(settings["db"]["CDIR"] + "/philoforces-db/" + settings["db"]["DBPATH"], "w") as f:
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

def help_common(isend = True):

    print(CLEARSCR, end="")

    print("Welcome to philoforces terminal edition." + BR(1) +
            "Commands are used in the following format: (cmd [-options]) [*args -> arg1 : arg2 : ...]:" + BR(1))

    print("(exit): leave." + BR(1))

    print("(mode) [mode-arg]: changes mode from user (user) to database editor (database)." + BR(1))

    print("(settings [-option]): change program settings" + BR(1) + INDENT(1) + 
                "-print [*args]: prints queried settings; leave empty to get all" + BR(1) + INDENT(1) + 
                "-change [setting] [arg]: changes setting to passed argument" + BR(1)
        )

    print("(clear): clears terminal of all previous queries" + BR(1))

    print("(open): opens question database" + BR(1) + INDENT(1) + 
                  "-online: queries file from git repo" + BR(1))

    print("(get) [pbcode]: opens problem associated to passed problem code" + BR(1))

    print("(list) [*args]: lists all problems available in current database, or problems in tags provided as arguments" + BR(1))

    # TODO: Implement random
    print("(toggle) [pbcode]: toggles status of problem associated to problem code to solved/unsolved" + BR(1))

    print("(random [-option]) [*args]: returns random question from either the full problemset or the ones in tags provided as arguments" + BR(1) + INDENT(1) + 
                "-unsolved: only picks unsolved questions from the pool" + BR(1)) 
    
    if(isend):
        input("Press Enter to reopen terminal.")
        print(CLEARSCREEN, end="")

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
                    for k in settings["user"]: print(k.ljust(10) + str(settings["user"][k]))

                if(not mode): print("")

            elif cmd[1] == "-change":

                if(args[0] in settings["user"]):
                    settings["user"][args[0]] = args[1]
                else:
                    print(f"Setting '{args[0]}' not found. No changes have been made.")

        case "open": 
            
            if(len(cmd) > 1):
                if(cmd[1] == "-online"): 
                    os.system("git clone https://github.com/Superomego-cloud/philoforces-db.git")
            init_database()

        case "get": open_problem(args[0])

        case "random":

            l = []
            if(not ("-tags" in cmd)):     
                    l = list(db["problems"].keys())
            else:

                if(not args):
                    print("No tags provided. Please try again.")
                    return

                for t in args:
                    if(t not in db["tags"]): continue
                    for p in db["tags"][t][1:]: l.append(p)

            if(not l): print("No problems to choose from. Load database with (open) or add problems in database mode.")
            elif(len(l) == 1): open_problem(l[0])
            else:
                r = random.randint(0, len(l) - 1)
                
                if(len(cmd) > 1):
                    if("-unsolved" in cmd):
                        while(sv[l[r]]["solved"]):
                            r = random.randint(0, len(l) - 1)
                
                open_problem(l[r])

        case "list":

            if(not db["problems"]):
                print("No problems to list.")
                return

            
            if not args: args = db["tags"].keys() 
            print("")

            for t in args:

                if(t not in db["tags"]): continue
                pbarr = db["tags"][t]

                if(len(pbarr) == 1): continue
                
                x, y, z = ((0, 255, 0) if pbarr[0] == len(pbarr) - 1 else 
                        ((255, 255, 0) if pbarr[0] else (255, 0, 0)))

                print(COLOR(f"{t}: [{pbarr[0]}/{len(pbarr) - 1}]", x, y, z) + BR(1))

                for p in pbarr[1:]:
                    
                    x, y, z = ((0, 255, 0) if sv[p]["solved"] else (255, 0, 0))
                    print(COLOR(p + ": " + db["problems"][p]["qst"], x, y, z))
                
                print("")

        case "toggle":

            try:
                sv[args[0]]["solved"] = not sv[args[0]]["solved"]
                db["tags"][db["problems"][args[0]]["mtag"]][0] += (1 if sv[args[0]]["solved"] else -1)
            except KeyError:
                print("Problem not found. Try again with correct problem name.")

        case "clear": 
            print(CLEARSCREEN, end="")

        case _:
            print("Command not found. Please try again.")


def user_mode(cmd, args):

    match cmd[0].lower():

        case "help": help_common() 
        case _:
            handle_common(cmd, args)


def db_mode(cmd, args):

    global is_saved

    match cmd[0].lower():

        case "help":
            
            help_common(False)

            print("===== ===== =====" + " ELEVATED COMMANDS " + "===== ===== =====" + BR(1))

            print("(set) [pbcode] : [question] : [file] : *[tags]: changes text entry associated to problem code to new file;" + " " 
                + "if problem code doesn't exist, it will be added to the database" + BR(1))

            print("(delete) [pbcode]: deletes entry associated to passed problem code" + BR(1))

            print("(tag) [pbcode] : [*args] adds tags to problem passed as argument." + BR(1) + INDENT(1) +
                    "-main: sets first argument as main tag" + BR(1) + INDENT(1) +
                    "-delete: removes all tags" + BR(1))

            print("(save): saves changes done to current database. Exit without saving to get unedited version" + BR(1) + INDENT(1)
                  + "-online: queries change to online repo via git; Only allowed for elevated git users. Make sure you are logged in." + BR(1))

            input("Press Enter to reopen terminal.")
            print(CLEARSCREEN, end="")

        case "settings":

            if cmd[1] == "-print": 

                handle_common(cmd, args)

                if args:
                    for k in args:     
                        try: 
                            print(k.ljust(10) + str(settings["db"][k]))
                        except KeyError: pass

                else: 
                    
                    print(BR(1) + "Database settings:" + BR(1))
                    for k in settings["db"]: print(k.ljust(10) + str(settings["db"][k]))
                    print("")

            elif cmd[1] == "-change":
                
                if(args[0] in settings["user"]):
                    settings["user"][args[0]] = args[1]
                elif (args[0] in settings["db"]):
                    settings["db"][args[0]] = args[1]
                else:
                    print(f"Setting '{args[0]}' not found. No changes have been made.")
                
        case "save": 

            save_database()

            if(len(cmd) > 1):
                if(cmd[1] == "-online"):
                
                    c = os.getcwd()
                    os.chdir(settings["db"]["CDIR"] + "/philoforces-db")
                    os.system("git add .")
                    os.system(f'git commit -m "Remote change done at {datetime.datetime.now().ctime()}"')
                    os.system("git branch -M main")
                    os.system("git remote rm philoforces-db")
                    os.system("git remote add philoforces-db https://github.com/Superomego-cloud/philoforces-db.git")
                    os.system(f"git push -u philoforces-db main")
                    os.chdir(c)

            is_saved = True

        case "set": 

            if(len(args) < 3): 
                print("Incorrect amount of arguments.")
                return

            if(args[0] in db["problems"]):
                delete_problem(args[0])

            create_problem(args[0], args[1], args[2], args[3:])
            is_saved = False

        case "tag":

            if(len(cmd) == 1):
                for t in args[1:]: 
                    if(t not in db["problems"][args[0]]["tags"]): db["problems"][args[0]]["tags"].append(t)
            else:
                
                if(cmd[1] == "-delete"):

                    db["tags"][db["problems"][args[0]]["mtag"]].remove(args[0])
                    db["problems"][args[0]]["mtag"] = "Ad hoc"
                    db["problems"][args[0]]["tags"] = []
                    db["tags"]["Ad hoc"].append(args[0])
                
                elif(cmd[1] == "-main"):

                    if(args[1] in db["problems"][args[0]]["tags"]): db["problems"][args[0]]["tags"].remove(args[1])
                    
                    if(sv[args[0]]["solved"]): 
                        db["tags"][db["problems"][args[0]]["mtag"]][0] -= 1
                        db["tags"][args[1]][0] += 1
                    

                    db["tags"][db["problems"][args[0]]["mtag"]].remove(args[0])
                    db["problems"][args[0]]["mtag"] = args[1]
                    if(args[1] not in db["tags"]): db["tags"][args[1]] = [0]
                    db["tags"][args[1]].append(args[0])

                    for t in args[2:]: 
                        if(t not in db["problems"][args[0]]["tags"]): db["problems"][args[0]]["tags"].append(t)
    


        case "delete":

            delete_problem(args[0])
            is_saved = False

        case _: user_mode(cmd, args)

print(CLEARSCREEN, end="")
load_settings()
load_save()
init_database()

while True:

    ip = (input(">>> ") + " ").split(") ")
    cmd = [w.strip() for w in ((ip[0])[1:]).split(" ")]
    args = []

    try:
        if(ip[1]): args = [w.strip() for w in ip[1].split(" : ")]
    except: pass

    try:

        match cmd[0].lower():

            case "exit": 

                if(settings["db"]["AUTOSAVE"]): save_database()
                
                elif(not is_saved): 

                    ip = input("It seems you have some unsaved changes. Would you like to save them? [Y/N]: ")
                    ip = ip.strip()
                    if(ip == "Y"): save_database()
                
                save_settings()
                save2()
                break


            case "mode":
                if(args[0] == "user"): mode = 0
                elif(args[0] == "database"): mode = 1

            case _:

                if(mode): db_mode(cmd, args)
                else: user_mode(cmd, args)

        bc = copy.deepcopy(db)

    except IndexError:
        print("Incorrect amount of arguments.")
    except:
        print(CLEARSCREEN, end="")
        print("There was an error handling this command. No changes have been made.")
        db = copy.deepcopy(bc)