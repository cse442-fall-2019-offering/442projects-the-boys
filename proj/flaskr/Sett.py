class Sett:
    def __init__(self, username, password, anon):
        self.username = username
        self.password = password
        self.anon = anon


    def setUserName(self, u):
        self.username = u

    def getUserName(self):
        return self.username

    def setPassword(self, p):
        self.password = p

    def getPassword(self):
        return self.password

    def setAnon(self, a):
        self.anon = a

    def getAnon(self):
        return self.anon

