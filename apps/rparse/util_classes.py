class Student(object):
    def __init__(self, roll_no, gender, name, subjects_list, result, misc_list):
        self.roll_no = roll_no
        self.gender = gender
        self.name = name
        self.subjects_dict = {}
        self.result = result
        self.misc_list = misc_list
        self.total_marks = 0

        for subject_data in subjects_list:
            sub_code = subject_data[0]
            distinct_subjects.add(sub_code)
            if len(subject_data) == 3:
                sub_marks, sub_grade = subject_data[1], subject_data[2]
                self.total_marks += int(sub_marks)
            else:
                print(
                    f"misc_list: {self.misc_list}, result: {self.result}, roll_no: {self.roll_no}"
                )
                sub_marks, sub_grade = "", ""

            self.subjects_dict[sub_code] = (sub_marks, sub_grade)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.roll_no, self.name, self.result)
