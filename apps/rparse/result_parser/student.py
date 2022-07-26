class Student(object):
    def __init__(self, student_dict):
        self.roll_no = student_dict["Roll No"]
        self.gender = student_dict["Gender"]
        self.name = student_dict["Name"]
        self.result = student_dict["Result"]
        self.misc_data = student_dict["Misc Data"]

        self.total_marks = 0
        self.subjects_dict = {}

        subject_keys = [
            "Subject 1",
            "Subject 2",
            "Subject 3",
            "Subject 4",
            "Subject 5",
            "Subject 6",
        ]

        for subject in subject_keys:
            subject_data = student_dict.get(subject)
            if subject_data is None or len(subject_data) < 3:
                continue
            sub_code = subject_data[0]
            if sub_code == "":
                continue

            sub_marks, sub_grade = subject_data[1], subject_data[2]
            if sub_marks.isnumeric():
                self.total_marks += int(sub_marks)

            self.subjects_dict[sub_code] = (sub_marks, sub_grade)

    def __str__(self):
        return f"{self.roll_no}-{self.name}-{self.result}"

    def __repr__(self):
        return f"{self.roll_no}-{self.name}-{self.result}"
