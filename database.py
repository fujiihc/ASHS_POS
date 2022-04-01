import pandas as pd

class database:
    def __init__(self):
        self.df = pd.DataFrame(columns = ['Name', 'SavedCourses'])

    def addInfo(self, name, courses):
        self.df = self.df.append(pd.DataFrame([[name, courses]], columns = ['Name', 'SavedCourses']), ignore_index = True)
    
    def getInfo(self, name):
       return self.df.loc[self.df['Name'] == name]

    def getDF(self):
        return self.df
    #creates database of users, their info, as well as their saved courses and whatnot
    #need a way to access, remove, update data
    #need a way to store files as well?
    #need a way to have persistent storage when the website is down. Maybe have like a save as thing that outputs a csv file before it shuts down
    #replace csv every shutdown as 'current data'
    #writing to the same csv files
    #just use pandas as an in between to access data from and write to the original csv
    #also consider using an sql database

    #create function to output a saved csv file upon shutdown for maintenance
    #frequent updates?
