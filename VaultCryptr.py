import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import hashlib
import time
import sqlite3

class Cryptr:

    path = os.getcwd()
    VaultDir = os.path.join(path, "Vault")
    InputDir = os.path.join(path, "Input")
    OutputDir = os.path.join(path, "Output")

    dbName = 'data.db'

    conn = sqlite3.connect(dbName)
    c = conn.cursor()

    def __init__(self):

        self.db_init()

        self.cls()

        self.checkDirectories()

        self.menu()

    def db_init(self):

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS Files
        (id INTEGER PRIMARY KEY,
        name TEXT, status TEXT
        )
        ''')

        self.conn.commit()

    def db_draw(self):

        return self.c.execute('SELECT * FROM FILES')

    def db_insert(self, filename, status):

        self.c.execute(f'''
        INSERT INTO Files(name, status) VALUES(?, ?)
        ''', (filename, status))

        self.conn.commit()


    def db_filter_name(self, filename):

        return self.c.execute('SELECT * FROM Files WHERE name = ?', (filename,))

    def db_filter_name_one(self, filename):

        self.c.execute('SELECT * FROM Files WHERE name = ?', (filename,))

        return self.c.fetchone()



    def db_filter_status(self, status):

        return self.c.execute('SELECT * FROM Files WHERE status = ?', (status,))

    def db_delete_filename(self, filename):

        self.c.execute('DELETE FROM Files WHERE name = ?', (filename,))

        self.conn.commit()

    def db_delete_status(self, status):

        self.c.execute('DELETE FROM Files WHERE status = ?', (status,))

        self.conn.commit()

    def db_reinit(self):

        self.c.execute('DROP TABLE IF EXISTS Files')

        self.conn.commit()

        self.db_init()

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def genHash(self):

        key = input("Define your password please: >>")
        key = hashlib.sha256(key.encode("utf-8")).digest()

        return key

    def menu(self):
        self.cls()
        print("What do you want to do?")

        print("1. Encrypt my Data")
        print("2. Decrypt my Data")
        print("3. Clean up")
        print("4. Advanced Database")
        print("5. Exit")

        option = input('>>')
        self.cls()


        if(option == '1'):
            # Encrypt Data

            bytefiles = self.getInputFiles(self.InputDir)
            key = ''
            if bytefiles:
                key = self.genHash()
                self.encryptData(key, bytefiles)
                print(f"Succesfully encrypted your Data with AES256 to: {self.VaultDir}")
                input("Press any key to continue...")
            else:
                print("No Files were found in: " + self.InputDir)
                time.sleep(2)
                self.cls()
            self.updateDatabase()
            self.menu()

        elif(option == '2'):
            # Decrypt Data

            bytefiles = self.getInputFiles(self.VaultDir)
            if bytefiles:
                key = self.genHash()

                self.decryptData(key, bytefiles)
            else:
                print("No Files were found in: " + self.VaultDir)
                time.sleep(2)
                self.cls()
            self.updateDatabase()
            self.menu()

        elif(option == '3'):
            # Clean all

            print("Do you really want to delete all Files within Input and Output?(Y/N)")
            if(input(">>").lower() == 'y'):
                print("deleting...")
                self.purgeDirs(self.InputDir)
                self.purgeDirs(self.OutputDir)
                self.db_reinit()
                time.sleep(1)
                print("Done!")
                input("Press any key to continue...")
            else:

                print("aborting...")
                time.sleep(1)
            self.updateDatabase()
            self.menu()

        elif(option == "4"):
            # Call Advanced Database Menu
            self.db_menu()

        elif(option == "5"):
            # Quit App
            quit()

        elif(option == ""):
            # Do Nothing
            self.menu()

        else:
            print("Command not found...")
            input()
            self.menu()

    def db_menu(self):
        # Advanced Database Menu
        self.cls()

        print("1. Insert Data")
        print("2. Delete Data (Filename)")
        print("3. Delete Data (Status)")
        print("4. Filter Database (Filename)")
        print("5. Filter Database (Status)")
        print("6. Draw Database")
        print("7. Reinitialize Database")
        print("8. Back")

        option = input(">>")

        if(option == "1"):
            # Insert Data

            self.cls()

            print("What Values do you want to input? (seperated by ';' ')")
            args = input(">>").split(';')
            self.db_insert(args[0], args[1])

            print("Done!")
            input("\nPress any Key to continue")
            self.db_menu()

        elif(option == '2'):
            # Delete Entries Filename
            self.cls()
            print("Specify the Filename")

            arg = input(">>")

            self.db_delete_filename(arg)

            print("Done!")
            input("\nPress any Key to continue")
            self.db_menu()

        elif(option == '3'):
            # Delete Entries Status

            self.cls()
            print("Specify the Status")

            arg = input(">>")

            self.db_delete_status(arg)

            print("Done!")
            input("\nPress any Key to continue")
            self.db_menu()

        elif(option == '4'):
            # Filter Filename

            self.cls()
            print("Specify the Name")

            arg = input(">>")

            for row in self.db_filter_name(arg):
                print(row)

            input("\nPress Any Key to continue")
            self.db_menu()

        elif(option == '5'):
            # Filter Filename

            self.cls()
            print("Specify the Status")

            arg = input(">>")

            for row in self.db_filter_status(arg):
                print(row)
            input("\nPress Any Key to continue")
            self.db_menu()

        elif(option == '6'):
            # Draw Database

            self.cls()
            for row in self.db_draw():
                print(row)
            input("\nPress Any Key to continue")
            self.db_menu()

        elif(option == '7'):
            # Reinitialize Database

            self.cls()
            self.db_reinit()
            print("Done!")
            input("\nPress Any Key to continue")
            self.db_menu()

        elif(option == '8'):
            # Exit to other menu

            self.menu()

        else:
            # do nothing
            self.db_menu()



    def purgeDirs(self, Directory):


        InputFiles = os.listdir(Directory)



        for filename in InputFiles:
            os.remove(os.path.join(Directory, filename))



    def checkDirectories(self):

        print(f"Current Directory is set to {self.path}")

        if not os.path.exists(self.VaultDir) or not os.path.exists(self.InputDir) or not os.path.exists(self.OutputDir):

            print(f"Could not find needed Directories in {self.path}!")

            print("Should I create your Vault Folders?\n(Y/N)")

            if(input(">>").lower() == 'y'):
                print("Ok i will do it")
                self.createDirs()

            else:
                print("ok shutting down...")
                quit()

        else:

            print("Found needed Directories!")

    def createDirs(self):

        try:
            if not os.path.exists(self.VaultDir):
                os.mkdir(self.VaultDir)
            if not os.path.exists(self.InputDir):
                os.mkdir(self.InputDir)
            if not os.path.exists(self.OutputDir):
                os.mkdir(self.OutputDir)
        except OSError:
            print("Something failed... Maybe run this script in root?")
        else:
            print("Succesfully created needed Directories!")

    def encryptData(self, key, bytefiles):

        encryptedFiles = {}

        #key = key.encode('ascii')
        cipher = AES.new(key, AES.MODE_CBC)

        i = 0

        for dic_key in bytefiles:
            enc = cipher.encrypt(pad(bytefiles[dic_key]['content'], AES.block_size))
            encryptedFiles[str(i)] = {}
            encryptedFiles[str(i)]['name'] = bytefiles[dic_key]['name'] + '.enc'
            encryptedFiles[str(i)]['content'] = enc
            encryptedFiles[str(i)]['iv'] = cipher.iv
            i+=1


        self.writeFiles(encryptedFiles, self.VaultDir)

    def decryptData(self, key, bytefiles):

        decryptedFiles = {}


        i = 0

        try:
            for dic_key in bytefiles:
                iv = bytefiles[dic_key]['iv']
                cipher = AES.new(key, AES.MODE_CBC, iv=iv)

                decrypted = cipher.decrypt(bytefiles[dic_key]['content'])
                unenc = unpad(decrypted, AES.block_size)
                decryptedFiles[str(i)] = {}
                decryptedFiles[str(i)]['name'] = bytefiles[dic_key]['name'].split('.enc')[0]
                decryptedFiles[str(i)]['content'] = unenc
                i+=1


            self.writeFiles(decryptedFiles, self.OutputDir)
            print(f"Succesfully decrypted your Data with AES256 to: {self.OutputDir}")
            input("Press any key to continue...")
        except ValueError:
            print("It seems that the Password you used was wrong...")
            time.sleep(1)
            input("Press any key to continue...")


    def writeFiles(self, files, Directory):

        for key in files:

            with open(os.path.join(Directory, files[key]['name']), 'wb') as f:
                if 'iv' in files[key]:
                    f.write(files[key]['iv'])
                f.write(files[key]['content'])

    def getInputFiles(self, Directory):

        filenames = os.listdir(Directory)


        if filenames:

            bytefiles = {}
            i = 0
            for filename in filenames:
                with open(os.path.join(Directory, filename), 'rb') as f:

                    bytefiles[str(i)] = {}
                    if '.enc' in filename:
                        bytefiles[str(i)]['iv'] = f.read(16)
                    bytefiles[str(i)]['name'] = filename
                    bytefiles[str(i)]['content'] = f.read()

                    i+=1

            return bytefiles

        else:
            return None

    def updateDatabase(self):


        for file in os.listdir(self.InputDir) + os.listdir(self.OutputDir) + os.listdir(self.VaultDir):
            if '.enc' in file:
                if not self.db_filter_name_one(file):
                    print("test")
                    self.db_insert(file, 'encrypted')
            else:
                if not self.db_filter_name_one(file):
                    self.db_insert(file, 'unencrypted')


if __name__ == "__main__":
    x = Cryptr()
