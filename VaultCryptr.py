import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import hashlib
import time

class Cryptr:

    path = os.getcwd()
    VaultDir = os.path.join(path, "Vault")
    InputDir = os.path.join(path, "Input")
    OutputDir = os.path.join(path, "Output")

    def __init__(self):
        self.cls()

        self.checkDirectories()

        self.menu()

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
        print("4. Exit")

        option = input('>>')
        self.cls()

        if(option == '1'):

            bytefiles = self.getInputFiles(self.InputDir)
            if bytefiles:
                key = self.genHash()
                self.encryptData(key, bytefiles)
                print(f"Succesfully encrypted your Data with AES256 to: {self.VaultDir}")
                input("Press any key to continue...")
            else:
                print("No Files were found in: " + self.InputDir)
                time.sleep(2)
                self.cls()
            self.menu()

        elif(option == '2'):


            bytefiles = self.getInputFiles(self.VaultDir)
            if bytefiles:
                key = self.genHash()

                self.decryptData(key, bytefiles)
            else:
                print("No Files were found in: " + self.VaultDir)
                time.sleep(2)
                self.cls()
            self.menu()

        elif(option == '3'):

            print("Do you really want to delete all Files within Input and Output?(Y/N)")
            if(input(">>").lower() == 'y'):
                print("deleting...")
                self.purgeDirs(self.InputDir)
                self.purgeDirs(self.OutputDir)
                time.sleep(1)
                print("Done!")
                input("Press any key to continue...")
            else:

                print("aborting...")
                time.sleep(1)
            self.menu()

        elif(option == "4"):
            quit()

        elif(option == ""):
            self.menu()

        else:
            print("Command not found...")
            input()
            self.menu()

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



if __name__ == "__main__":
    x = Cryptr()
