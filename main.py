from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
import sqlite3
from random import randint

Config.set('graphics', 'width', '300')

class DBAdministrator():
    
    def connecting(self):
        """Connect to database and save conection and cursor on variables

        Args:
            database (str, optional): name of the database to conect to. Defaults to "repo.db".
        """
        try:
            conection = sqlite3.connect("repo.db")
            cursor = conection.cursor()
            return (conection,cursor)
        except Exception as e:
            print ("Error, ",e)

    def execute(self,command):
        """Run a command in the database

        Args:
            command (string):sqlite command.
        """
        sq = self.connecting()
        conection = sq[0]
        cursor = sq[1]
        try:
            cursor.execute(command)
            conection.commit()
            
            return cursor
        except Exception as e:
            print(f"--Error:{e}")
            self.disconnect(conection)

    def disconnect(self,conection):
        """Disconect from the database
        """
        conection.close()
    


class Creator(Screen):
    encript = ObjectProperty(False)
    user = ObjectProperty(False)
    site = ObjectProperty(False)
    
    def checkbox_click(self):
        self.encript = not self.encript
    
    def InsertPassword(self):
        siteInfo = self.site.text
        userInfo = self.user.text
        if len(siteInfo) > 0  and len(userInfo) >0:
            password = self.CreatePass()
            id = self.getID()

            if self.encript == True:
                en = 1
            else:
                en = 0

            dba.execute(f"INSERT INTO passwords VALUES('{id}','{siteInfo}','{userInfo}','{password}','{en}')")
    
    def getID(self):
        cursor = dba.execute("SELECT COUNT (*) FROM passwords")
        count = cursor.fetchall()

        print(len(count))

        if len(count) == 0:
            return 1
        
        else:
            cursor = dba.execute("SELECT id FROM passwords ORDER BY id")
            data = cursor.fetchall()
            number = 1

            for num in data:
                if num != number and num > number:
                    return number
                else:
                    number +=1

    def CreatePass(self):
        lowerLetters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        UpperLetters=['A', 'B', 'C', 'D', 'E', 'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        symbols=['|','#','$','&','%','/','-','+','_']
        password=self.process(lowerLetters,UpperLetters,symbols)
        return password

    def process(self,lowerLetters,UpperLetters,symbols):
        final='' #Create empty string to store password
        for i in range(30):#Create a password with 30 characters
            key=randint(1,1000)#Chooses a number between 1 and 1000
            #first checks if the number can be devided by 2
            if (key%2)==0:
                #It will add a random character from a specific list of characters
                #depending if the "key" is greater of smaller then 500
                if key<=500:
                    #uselower
                    temp=lowerLetters[randint(0,len(lowerLetters)-1)] 
                    #choose a character without overlapping ammount of characters available
                if key>500:
                    #useupper
                    temp=UpperLetters[randint(0,len(UpperLetters)-1)]
            else: #If it is not divisible by 2 it will do the same process but with different characters
                if key<=500:
                    #useNumber
                    temp=str(randint(0,10))
                if key>500:
                    #useSymbol
                    temp=symbols[randint(0,len(symbols)-1)]

            #Adds selected character to the final string
            final+=temp
        return final


#stuff for login page
class LoginLayout(Screen):
    #user input password
    key = ObjectProperty(None)

    def __init__(self, **kw):
        super(LoginLayout,self).__init__(**kw)

    def obtainPass (self):
        keyPass = self.key.text
        if len(keyPass) >0:
            self.changeScreen()
    
    def changeScreen(self):
        if self.manager.current == "loginPage":
            self.manager.current = "createPage"
        else:
            self.manager.current = "loginPage"

#Declare Screens
class Manager(ScreenManager):
    loginScreen = ObjectProperty(None)
    createScreen = ObjectProperty(None)

#Builder
class PassManager(App):
    def build(self):
        m = Manager(transition = NoTransition())
        return m

if __name__ == '__main__':
   dba = DBAdministrator()
   app = PassManager()
   app.run()
   dba.disconnect()