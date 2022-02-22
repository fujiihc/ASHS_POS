import pandas as pd


class data:
    def __init__(self):
        self.df = pd.read_csv('courses.csv', encoding = 'latin1')
        #self.df.columns = ['Course','Short Description','Curriculumn','Len', 'Crs Typ', 'Dept Cd', 'Earned Crdts', 'Grade Req Crdts', 'Grd L', 'Grd H', 'T G']

    def getCourse(self, courseName):
       return self.df.loc[self.df['CourseName'].str.contains(courseName, na = False)]
   
