from polyalphabetics import viginere
import polyalphabetics as p
import random
from Tkinter import Tk
import os

def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

class Core:
    alphabet = "".join([chr(i) for i in range(0, 255)])
    
    def __init__(self, db_file, master_password):
        self.master_password = master_password
        self.db_file = db_file

    def load_db(self):
        try:
            inp = open(self.db_file, "r")
            data = inp.read()
            inp.close()
        except:
            self.rows = {}
            return None
        rows = {}
        data = self.decrypt(data, self.master_password)
        for line in data.split("\n"):
            if len(line)>0:
                key, value = line.split("|")
                rows[key] = value
        self.rows = rows
        return rows

    @classmethod
    def decrypt(self, data, password):
        return viginere(data, password, alphabet=self.alphabet, enc=False)

    @classmethod
    def encrypt(self, data, password):
        return viginere(data, password, alphabet=self.alphabet, enc=True)

    def generate_password(self):
        n = 100
        s = ""
        while n>0:
            s += str(random.randint(0, 9))
            n -= 1
        return s

    def get_all_keys(self):
        return self.rows.keys()

    def get_password(self, key):
        return self.rows[key]

    def copy_password_to_clipboard(self, key):
        addToClipBoard(self.rows[key])

    def create_password(self, name):
        pwd = self.generate_password()
        assert name not in self.rows.keys()
        assert name.count("|") == 0
        self.rows[name] = pwd
        self.save()
        return name, pwd

    def remove_password(self, name):
        assert name in self.rows.keys()
        del self.rows[name]
        self.save()

    def save(self):
        text = ""
        for key, value in self.rows.items():
            text += "%s|%s\n" % (key, value)
        text = self.encrypt(text, self.master_password)
        with open(self.db_file, "w") as inp:
            inp.write(text)

class Terminal:
    version = "0.1.0"
    name = "Passi - Password Manager"
    current_algorithm = "Vigenere"
    commands = {
        "UNLOCK": ["open db"],
        "LOCK": ["close db"],        
        "INIT": ["start new db"],
        "GEN": ["add pwd"],
        "GET": ["get pwd"],
        "ALL": ["get all names"],
        "REM": ["remove pwd"],
        "COPY": ["copy pwd to clipboard"],
        "HELP": ["display all commands"],
        "QUIT": ["exit with saving"]
        }
    state = "NOTHING LOADED"
    core = None
    
    def __init__(self):
        pass

    def print_hello(self):
        print("Welcome to %s @ version %s\nCurrent algorithm: %s\n"
              % (self.name, self.version, self.current_algorithm) + "-"*80)

    def print_commands(self):
        print("LIST OF COMMANDS:\n"+"\n".join(["-%s\t(%s)" % (key, value[0]) for key, value in self.commands.items()]))

    def print_crypto_test(self):
        s = "".join([chr(random.randint(0, 255)) for i in range(100)])
        print("CRYPTOTEST")
        print("RAW=" + s)
        print("CIP=" + Core.encrypt(s, "123456789"))
        print("REC=" + Core.decrypt(Core.encrypt(s, "123456789"), "123456789"))
        print("~"*80)
        

    def prompt(self):
        print("-"*80)
        print(self.name)
        print(self.state)
        inp = raw_input("==>")
        if inp not in self.commands.keys():
            self.print_commands()
            return
        if inp == "HELP":
            self.print_commands()
            return
        if inp == "QUIT":
            print("BYE")
            quit()
        if self.state == "NOTHING LOADED":
            if inp in ("LOCK", "GEN", "GET", "ALL", "REM", "COPY"):
                print("INVALID COMMAND. You cannot manipulate a not opened db.")
                return
            else:
                if inp in ("UNLOCK", "INIT"):
                    self.core = Core(raw_input("db_file:"), raw_input("master_password:"))
                    print("try to load db...")
                    self.core.load_db()
                    print("Core is ready!")
                    self.state = "DB (%s) LOADED" % (self.core.db_file)
                    return
                else:
                    print("MISSING IMPLEMENTATION (->REPORT BUG")
                    return
        else:
            if inp == "LOCK":
                print("Locking and leaving the current db...")
                del self.core
                self.core = None
                self.state = "NOTHING LOADED"
                return
            elif inp == "GEN":
                print("Enter the account's name, like Facebook or github")
                name = raw_input("Name:")
                print(self.core.create_password(name))
                print("DB saved...")
                return
            elif inp == "GET":
                name = raw_input("Name:")
                print(self.core.get_password(name))
                return
            elif inp == "ALL":
                print("\n".join(self.core.get_all_keys()))
                return
            elif inp == "REM":
                name = raw_input("Name:")
                print(self.core.remove_password(name))
                print("DB saved...")
                return
            elif inp == "COPY":
                name = raw_input("Name:")
                self.core.copy_password_to_clipboard(name)
                print("Password is in clipboard")
                return
            else:
                print("Missing Implementation or INVALID COMMAND (like INIT) at this stage")

    def mainloop(self):
        self.print_crypto_test()
        self.print_hello()
        while True:
            self.prompt()


if __name__ == '__main__':
    Terminal().mainloop()
                
                
        
            
        
        
        
                    
