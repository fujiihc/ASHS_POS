import pandas as pd

class data:
    def __init__(self):
        self.df = pd.read_csv('abCourseData.csv', encoding='cp1252')
        
    def getCourse(self, keywords, searchCol):
       return self.df.loc[self.searchCheck(keywords.split(' '), self.df['longDescription'].str.split(' '))]

    def searchCheck(self, keyArr, searchArr):
        finalList = []
        for item in searchArr:
            toAdd = False
            checkArr = []
            for search in keyArr:
                for word in item:
                    if search in word:
                        toAdd = True
                        break
                checkArr.append(toAdd)
                toAdd = False
            toAdd = True
            for boolean in checkArr:
                if boolean == False:
                    toAdd = False
                    break
            finalList.append(toAdd)   
        return finalList
