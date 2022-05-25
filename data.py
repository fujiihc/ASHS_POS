import pandas as pd

class data:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def findCourse(self, keywords, searchCol, exact):
        thingy1 = keywords.split(' ')
        thingy2 = self.df[searchCol].str.split(' ')
        if exact:
            thingy1 = [keywords]
            thingy2 = list(self.df[searchCol])
        return data(self.df.loc[self.searchCheck(thingy1, thingy2, exact)])

    def getDF(self):
        return self.df

    def searchCheck(self, keyArr, searchArr, exact):     
        finalList = []       
        for item in searchArr:         
            toAdd = False
            checkArr = []      
            for search in keyArr:
                if not exact:
                    for word in item: 
                        if search in word:
                            toAdd = True
                            break
                else:
                    if search == item:               
                        toAdd = True
                checkArr.append(toAdd)
                toAdd = False
            toAdd = True
            for boolean in checkArr:
                if boolean == False:
                    toAdd = False
                    break
            finalList.append(toAdd)   
        return finalList

    def merge(self, data2):
        self.df = pd.concat([self.df, data2.getDF()]).drop_duplicates().reset_index(drop = True)
        return self
        
