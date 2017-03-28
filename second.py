import zipfile

zFile = zipfile.ZipFile("window.zip")
passFile = open("passwords.txt")

for line in passFile.readlines():
    try:
        password = line.strip('\n').encode()
        print(str(password))
        zFile.extractall(pwd=password)
        print("[+] Password = " + str(password) + "\n")
        exit()
    except RuntimeError:
        pass
    except zipfile.BadZipfile:
        pass
    except Exception as e:
        pass