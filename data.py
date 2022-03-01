import pandas as pd

class data:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def findCourse(self, keywords, searchCol):
       return data(self.df.loc[self.searchCheck(keywords.split(' '), self.df[searchCol].str.split(' '))])

    def getDF(self):
        return self.df

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
