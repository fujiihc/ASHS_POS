import pandas as pd

class data:
    def __init__(self):
        self.df = pd.read_csv('22-23CourseMaster.csv')
        #self.df.columns = ['Course','Short Description','Curriculumn','Len', 'Crs Typ', 'Dept Cd', 'Earned Crdts', 'Grade Req Crdts', 'Grd L', 'Grd H', 'T G']

    def getCourse(self, courseName):
       return self.df.loc[self.df['Short Description'].str.contains(courseName, na = False)]
   
