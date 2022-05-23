import sqlite3

class database:

    def __init__(self, name):
        self.name = name
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            idNum TEXT PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            courses TEXT NOT NULL,
            token TEXT NOT NULL,
            isLoggedIn TEXT NOT NULL,
            counselors TEXT NOT NULL);''')

        connection.commit()
        connection.close()

    def addData(self, idNum, email, firstName, lastName, courses, token, isLoggedIn, counselors):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        coursesStr = ''
        for num in range(len(courses)):
            coursesStr += courses[num]
            if not num == len(courses) - 1:
                coursesStr += '#'
        isLoggedInStr = ''
        if isLoggedIn:
            isLoggedInStr = 'True'
        else:
            isLoggedInStr = 'False'
        valuesList = (str(idNum),str(email), str(firstName), str(lastName), str(coursesStr), str(token), str(isLoggedInStr), str(counselors))
        try:
            cursor.execute('INSERT INTO "users" VALUES (?,?,?,?,?,?,?,?)', valuesList)
            connection.commit()
        except:
            return False
        connection.close()
        return True

    def findData(self, idNum):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        thingy = (str(idNum),)
        try:
            cursor.execute('SELECT * FROM "users" WHERE "idNum" = ?', thingy)     
        except:
            return False
        thingy2 = cursor.fetchall()
        connection.close()
        return thingy2
        
    def deleteData(self, idNum):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        thingy = (str(idNum),)
        try:
            cursor.execute('DELETE FROM "users" WHERE "idNum" = ?', thingy)
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False
        
    def dataList(self):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        finList = []
        for row in cursor.execute('SELECT * FROM "users"'):
            #comment out later
            print(row)
            finList.append(row)
        connection.close
        return finList
