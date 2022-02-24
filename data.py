import pandas as pd


class data:
    def __init__(self):
        self.df = pd.read_csv('abCourseData.csv', encoding='cp1252')
        
    def getCourse(self, keywords, searchCol):
       return self.df.loc[self.searchCheck(keywords.split(' '), self.df['longDescription'].str.split(' '))]

   #returns a boolean array
   #edit to take fragments that aren't the same length as the results
   #doing so could result in one return statement for getCourse()
   #maybe like a rolling check?
   #or maybe like i guess being able to include multiple keywords by including a multi keyword checker num in getCourse like keyword Num and I could run a for loop
    def searchCheck(self, keyArr, searchArr):
        finalList = []
        for item in searchArr:
            toAdd = False
            check = []
            for search in keyArr:
                for word in item:
                    if search in word:
                        toAdd = True
                check.append(toAdd)
                toAdd = False
            toAdd = True
            for boolean in check:
                if boolean == False:
                    toAdd = False
                    
            #have to make sure that all keywords are contained within the results and only those ones
            finalList.append(toAdd)   
        return finalList
