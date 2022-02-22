import pandas as pd


class data:
    def __init__(self):
        self.df = pd.read_csv('courses.csv', encoding='cp1252')
        #change encoding
        
    def getCourse(self, keyword, searchCol):
       return self.df.loc[self.df[searchCol].str.contains(keyword, na = False)]
