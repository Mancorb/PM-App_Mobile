from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
import sqlite3
import plyer
from random import randint

Config.set('graphics', 'width', '300')

class DBAdministrator():
    def __init__(self):
        self.con = sqlite3.connect("repo.db")
        self.cursor = self.con.cursor()

    def execute(self,command):
        """Run a command in the database

        Args:
            command (string):sqlite command.
        """
        try:
            self.cursor.execute(command)
            self.con.commit()
            
        except Exception as e:
            print(f"--Error:{e}\nConextion terminated")
            self.con.close()

    def disconnect(self):
        """Disconect from the database
        """
        self.con.close()
    


class Creator(Screen):
    encript = ObjectProperty(False) #flag to encript password
    user = ObjectProperty(False) #store username input
    site = ObjectProperty(False) #store website name input
    alert = ObjectProperty(False) #notification
    
    def checkbox_click(self):
        """Flip the state of the flag
        """
        self.encript = not self.encript
    
    def InsertPassword(self):
        dba = DBAdministrator()

        siteInfo = self.site.text
        userInfo = self.user.text
        
        if len(siteInfo) > 0  and len(userInfo) >0:
            password = self.CreatePass()
            id = self.getID(dba)

            if self.encript == True:
                en = 1
            else:
                en = 0

            dba.execute(f"INSERT INTO passwords VALUES('{id}','{siteInfo}','{userInfo}','{password}','{en}')")
            dba.disconnect()

            self.site.text = ""
            self.user.text =""
            plyer.notification.notify(title="Update", message=f"Inserted password for {siteInfo}")

    
    def getID(self,dba):
        """Find corresponding id for insertion

        Args:
            dba (DBAdministrator object): object that has conection to the database

        Returns:
            int: id for the insertion
        """
        dba.execute("SELECT COUNT (*) FROM passwords")
        count = dba.cursor.fetchall()

        if count[0][0] == 0:
            return 1
        
        else:
            dba.execute("SELECT id FROM passwords ORDER BY id")
            data = dba.cursor.fetchall()
            number = 1

            for i in range(len(data)):
                id = data[i][0]
                if id == number:
                    number +=1
                else:
                    return number
            
            return number

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
   app = PassManager()
   app.run()