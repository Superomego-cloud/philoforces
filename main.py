import os, json, random, datetime

db = {}
settings = {}
random.seed()
os.system("")

DEFAULT = {"OPENFILE":True, "AUTOSAVE":False, "ONLINE":True, "WEB": "", "CDIR": os.getcwd(), "DBPATH": "db.json"}
INDENT = lambda n: "\t"*n
BR = lambda n: "\n"*n
SPACE = lambda n: " "*n 
QST = lambda q, f: {"qst": q, "file": f}
is_saved = True

def open_problem(pcode):

    global db

    print("")

    try: print(pcode + ": " + db["problems"][pcode]["qst"])
    except: 
        print("Problem code not found. Reload database with (open) or add entry with (set). See (help) for instructions." + BR(1))
        return

    if settings["OPENFILE"]:
        
        input("Press [Enter] to open file" + BR(1))

        try: 
            f = open(os.getcwd() + "/question_pool/" + db["problems"][pcode]["file"], "x")
            f.close()
        except: 
            pass

        os.startfile(os.getcwd() + "/question_pool/" + db["problems"][pcode]["file"])

def init_database():
    
    global db

    try: 
        with open(settings["DBPATH"], "r") as f:
            db = json.load(f)

    except: print("could not find JSON database." + " " 
                + f"Make sure {settings['DBPATH']} is in current directory ({settings['CDIR']})" + " "
                + "or change current directory / database file path with" + " "
                + "(settings -change) CDIR [dir] / (settings -change) DBPATH [dir]"
                )

def load_web(): 
    
    # queries either google drive or git for a cool file you need
    
    return 

def save_database():

    global db

    try:
        with open(settings["DBPATH"], "w") as f:
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

print("\x1b[2J\x1b[HPHILOFORCES TERMINAL EDITION V0")
print("Made by yours truly. Print (help) for instructions." + BR(1))
load_settings()
init_database()

while True:

    ip = (input(">>> ") + " ").split(") ")
    cmd = [w.strip() for w in ((ip[0])[1:]).split(" ")]

    if(ip[1]): args = [w.strip() for w in ip[1].split(" : ")]

    match cmd[0].lower():

        case "help":

            print(BR(1) + "Welcome to philoforces terminal edition.\n" +
                  "Commands are used in the following format: (cmd [-options]) [*args -> arg1 : arg2 : ...]:" + BR(1))

            print("(exit): leave." + BR(1))
            
            print("(settings [-option]): change program settings" + BR(1) + INDENT(1) + 
                    "-print [*args]: prints queried settings" + BR(1) + INDENT(1) + 
                    "-change [setting] [arg]: changes setting to passed argument" + BR(1)
            )
            
            print("(random [-option]) [*args]: returns random question" + BR(1) + INDENT(1) + 
                    "-tags [*args]: returns random question with any one of the tags passed as argument" + BR(1) + INDENT(1) + 
                    "-philosophers [*args]: returns random question with any one of the passed philosophers" + BR(1)
            )
            
            print("(get) [pbcode]: opens problem associated to passed problem code" + BR(1))
            
            print("(set) [pbcode] : [question] : [file]: changes text entry associated to problem code to new file;" + " " 
                + "if problem code doesn't exist, it will be added to the database" + BR(1))
            
            print("(delete) [pbcode]: deletes entry associated to passed problem code" + BR(1))
            
            print("(save): saves changes done to current database. Exit without saving to get unedited version" + BR(1) + INDENT(1)
                  + "-online: queries change to online repo via git; Only allowed for elevated git users." + BR(1))
            
            print("open: opens question database" + BR(1) + INDENT(1) + 
                  "-online: queries file from git repo" + BR(1))

        case "cdir":

            if cmd[1] == "-print": print(os.getcwd())
            else: os.chdir(args[0])

        case "exit": 
            
            if(settings["AUTOSAVE"]): save_database()
            elif(not is_saved): 

                ip = input("It seems you have some unsaved changes. Would you like to save them? [Y/N]: ")
                ip = ip.strip()

                if(ip == "Y"): save_database()
                
            exit()

        case "restart": init_database()

        case "save": 

            if(len(cmd) > 1):
                if(cmd[1] == "-online"): 
                    os.system(f"git commit -m 'Automatic change at {datetime.datetime.now().ctime()}'")
                    os.system(f"git push philoforces")

            save_database()

        case "get": open_problem(args[0])

        case "set": 
            db["problems"][args[0]] = QST(args[1], args[2])
            is_saved = False

        case "delete":

            del db["problems"][args[0]]
            is_saved = False
