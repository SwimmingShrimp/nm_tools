class Student(object):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Student Object is {self.name}"

s = Student("lilei")
print(s)