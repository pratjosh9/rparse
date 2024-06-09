class Student(object):
    def __init__(self, unique_id_1, unique_id_2, name, gender, result, subjects):
        self.unique_id_1 = unique_id_1
        self.unique_id_2 = unique_id_2
        self.name = name
        self.gender = gender
        self.result = result
        self.subjects = subjects

    def __str__(self):
        return f"{self.unique_id_1}-{self.name}-{self.result}-{self.subjects}"

    def __repr__(self):
        return f"{self.unique_id_1}-{self.name}-{self.result}-{self.subjects}"
