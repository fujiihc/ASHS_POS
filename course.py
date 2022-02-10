class course:
    def __init__(self, name, ID, desc, days, lvl, len, grade, credits):
        self.name = name
        self.ID = ID
        self.desc = desc
        self.days = days
        self.lvl = lvl
        self.len = len
        self.grade = grade
        self.credits = credits


    def getCourseData(self):
        return [self.name, self.ID, self.desc, self.days, self.lvl, self.len, self.grade, self.credits]
