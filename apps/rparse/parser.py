from .constants import subject_code_dict_class_12, subject_code_dict_class_10
from .constants import student_marks_idxs_dict, student_marks_idxs
from .constants import student_details_idxs_dict, student_details_idxs


def write_worksheet(workbook, worksheet_name, fields, data_list):
    worksheet = workbook.add_worksheet(worksheet_name)
    worksheet.write_row(0, 0, fields)
    for idx, data in enumerate(data_list):
        worksheet.write_row(idx + 1, 0, data)


def clean_line(line):
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), line.split(" "))))


def get_student(student_line, marks_line, distinct_subjects):
    student_split = clean_line(student_line)
    marks_split = clean_line(marks_line)
    student_data = {}
    student_data["Roll No"] = student_split[0]
    student_data["Gender"] = student_split[1]

    name_list = []
    idx = 2
    while idx < len(student_split) and not student_split[idx].isnumeric():
        name_list.append(student_split[idx])
        idx += 1
    student_data["Name"] = " ".join(name_list)

    subject_idx = 1
    while idx < len(student_split) and student_split[idx].isnumeric():
        subject_key = f"Subject {subject_idx}"
        distinct_subjects.add(student_split[idx])
        student_data[subject_key] = [student_split[idx]]
        idx += 1
        subject_idx += 1

    while idx < len(student_split) and len(student_split[idx]) <= 2:
        idx += 1

    student_data["Result"] = student_split[idx]

    student_data["Compartment Subjects"] = (
        "" if idx + 1 == len(student_split) else " ".join(student_split[idx + 1 :])
    )

    for idx in range(len(marks_split)):
        subject_idx = idx // 2 + 1
        subject_key = f"Subject {subject_idx}"
        student_data[subject_key].append(marks_split[idx])

    return Student(student_data)


class Student(object):
    def __init__(self, student_dict):
        self.roll_no = student_dict["Roll No"]
        self.gender = student_dict["Gender"]
        self.name = student_dict["Name"]
        self.result = student_dict["Result"]
        self.comp_subjects = student_dict["Compartment Subjects"]

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
        return "{0}-{1}-{2}".format(self.roll_no, self.name, self.result)


class ResultParser(object):
    def parse_lines(self, lines):
        students_list = []
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            idx += 1

            if not line[0].isnumeric():
                continue

            mark_line = lines[idx]
            students_list.append(get_student(line, mark_line, self.distinct_subjects))
            idx += 1
        return students_list

    def parse_result(self):
        if len(self.students_list) == 0:
            raise ValueError("No Students Found")
        for sub_code in self.distinct_subjects:
            self.get_subject_wise_list(sub_code)

        self.write_school_pi()
        self.write_section_list()

    def __init__(self, lines, workbook, class_std):
        self.class_std = class_std
        self.subject_code_dict = (
            subject_code_dict_class_10
            if (class_std == "10")
            else subject_code_dict_class_12
        )
        self.grades_dict = {}

        self.workbook = workbook
        self.distinct_subjects = set()
        self.students_list = self.parse_lines(lines)
        # print("Number of students ", len(students_list))
        self.parse_result()
        self.workbook.close()

    def get_section_data(self, subject_list, mandatory_subject, section_name):
        fields = ["Student Name"]
        for subject_code in subject_list:
            fields.extend(
                [
                    f"{self.subject_code_dict[subject_code]}_marks",
                    f"{self.subject_code_dict[subject_code]}_grade",
                ]
            )
        fields.extend(
            [f"Total Marks{len(subject_list)*100}", "Result", "Compartment Data"]
        )

        section_data = []

        for idx, student in enumerate(self.students_list):
            current_total = 0
            if mandatory_subject not in student.subjects_dict:
                continue
            data = [student.name]
            for subject_code in subject_list:
                subject_data = student.subjects_dict.get(subject_code, ["", ""])
                marks, grade = subject_data[0], subject_data[1]
                if marks.isnumeric():
                    marks = int(marks)
                    current_total += marks
                data.extend([marks, grade])

            data.extend([current_total, student.result, student.comp_subjects])
            section_data.append(data)

        write_worksheet(self.workbook, section_name, fields, section_data)

    def write_section_list(self):
        if self.class_std == "12":
            arts = ["301", "302", "027", "029", "028", "030"]
            science = ["301", "302", "044", "043", "042", "041", "083"]
            commerce = ["301", "302", "030", "055", "054", "041", "065"]

            self.get_section_data(arts, "027", "Arts")
            self.get_section_data(science, "042", "Science")
            self.get_section_data(commerce, "055", "Commerce")
        else:
            self.get_section_data(
                self.distinct_subjects, list(self.distinct_subjects)[0], "Class X"
            )

    def write_school_pi(self):
        grades_list = [
            ("A1", 8),
            ("A2", 7),
            ("B1", 6),
            ("B2", 5),
            ("C1", 4),
            ("C2", 3),
            ("D1", 2),
            ("D2", 1),
            ("E", 0),
        ]

        fields = ["Grade", "Frequency"]

        pi_data, pi_value = [], 0
        frequency = 0
        for grade, weightage in grades_list:
            count = self.grades_dict.get(grade, 0)
            frequency += count
            pi_data.append([grade, count])
            pi_value += weightage * count

        pi_value /= frequency * 8
        pi_data.append(["pi", pi_value * 100])

        worksheet_name = "School PI"
        write_worksheet(self.workbook, worksheet_name, fields, pi_data)

    def write_pi_list(self, subject_list, sub_code):
        grades_list = [
            ("A1", 8),
            ("A2", 7),
            ("B1", 6),
            ("B2", 5),
            ("C1", 4),
            ("C2", 3),
            ("D1", 2),
            ("D2", 1),
            ("E", 0),
        ]
        grades_dict = {}
        for data in subject_list:
            grade = data[3]
            if grade not in grades_dict:
                grades_dict[grade] = 0
            grades_dict[grade] += 1

        fields = ["Grade", "Frequency"]

        pi_data, pi_value = [], 0
        frequency = 0
        for grade, weightage in grades_list:
            count = grades_dict.get(grade, 0)
            frequency += count
            if grade not in self.grades_dict:
                self.grades_dict[grade] = 0
            self.grades_dict[grade] += count
            pi_data.append([grade, count])
            pi_value += weightage * count

        pi_value /= frequency * 8
        pi_data.append(["pi", pi_value * 100])
        worksheet_name = f"{self.subject_code_dict[sub_code]}_PI"
        write_worksheet(self.workbook, worksheet_name, fields, pi_data)

    def get_subject_wise_list(self, sub_code):
        subject_list_fields = ["Roll No", "Student Name", "Marks", "Grade"]
        subject_list = []
        for student in self.students_list:
            if sub_code not in student.subjects_dict:
                continue
            sub_marks, sub_grade = (
                student.subjects_dict[sub_code][0],
                student.subjects_dict[sub_code][1],
            )

            if sub_marks == "":
                continue

            subject_data = [student.roll_no, student.name, int(sub_marks), sub_grade]
            subject_list.append(subject_data)

        write_worksheet(
            self.workbook,
            self.subject_code_dict[sub_code],
            subject_list_fields,
            subject_list,
        )
        self.write_pi_list(subject_list, sub_code)


# def get_student(student_line, marks_line, distinct_subjects):
#     student_data = {}
#     for idx, file_idx in enumerate(student_details_idxs):
#         name = student_details_idxs_dict[file_idx]
#         next_idx = (
#             student_details_idxs[idx + 1] if idx + 1 < len(student_details_idxs) else -1
#         )
#         if next_idx != -1:
#             data = student_line[file_idx - 1 : next_idx - 1]
#         else:
#             data = student_line[file_idx - 1 :]
#         student_data[name] = data.strip()

#     diff = 2 if marks_line[student_marks_idxs[0]-2].isnumeric() else 1
#     # print("Diff ", diff)
#     for idx, file_idx in enumerate(student_marks_idxs):
#         name = student_marks_idxs_dict[file_idx]
#         next_idx = (
#             student_marks_idxs[idx + 1] if idx + 1 < len(student_marks_idxs) else -1
#         )
#         if (file_idx-diff >= len(marks_line)):
#             continue

#         if next_idx != -1:
#             data = marks_line[file_idx - diff : next_idx - diff]
#         else:
#             data = marks_line[file_idx - diff :]
#         if not isinstance(student_data[name], list):
#             if student_data[name] != "":
#                 distinct_subjects.add(student_data[name])
#             student_data[name] = [student_data[name]]
#         student_data[name].append(data.strip())
#         # print(student_data)
#     return Student(student_data)
