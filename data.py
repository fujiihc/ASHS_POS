import pandas as pd
import course

class data:
    def __init__(self):
        self.df = pd.DataFrame(columns = range(8))
        self.df.columns = ['Name','ID','Description','Days/Week', 'Level', 'Length', 'Grade', 'Credits']

    def addCourse(self, course):
        self.df.loc[len(self.df.index)] = course.getCourseData()

    def toString(self):
        return self.df.to_string()
