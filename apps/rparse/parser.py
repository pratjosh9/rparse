from .constants import subject_code_dict_class_12, subject_code_dict_class_10
from .constants import student_marks_idxs_dict, student_marks_idxs
from .constants import student_details_idxs_dict, student_details_idxs


def write_worksheet(workbook, worksheet_name, fields, data_list):
    worksheet = workbook.add_worksheet(worksheet_name)
    worksheet.write_row(0, 0, fields)
    for idx, data in enumerate(data_list):
        worksheet.write_row(idx + 1, 0, data)


def get_student(student_line, marks_line, distinct_subjects):
    student_data = {}
    for idx, file_idx in enumerate(student_details_idxs):
        name = student_details_idxs_dict[file_idx]
        next_idx = (
            student_details_idxs[idx + 1] if idx + 1 < len(student_details_idxs) else -1
        )
        if next_idx != -1:
            data = student_line[file_idx - 1 : next_idx - 1]
        else:
            data = student_line[file_idx - 1 :]
        student_data[name] = data.strip()

    for idx, file_idx in enumerate(student_marks_idxs):
        name = student_marks_idxs_dict[file_idx]
        next_idx = (
            student_marks_idxs[idx + 1] if idx + 1 < len(student_marks_idxs) else -1
        )
        if next_idx != -1:
            data = marks_line[file_idx - 1 : next_idx - 1]
        else:
            data = marks_line[file_idx - 1 :]

        if not isinstance(student_data[name], list):
            if student_data[name] != "":
                distinct_subjects.add(student_data[name])
            student_data[name] = [student_data[name]]
        student_data[name].append(data.strip())

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
            subject_data = student_dict[subject]
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

        self.write_section_list()

    def __init__(self, lines, workbook, class_std):
        self.class_std = class_std
        self.subject_code_dict = (
            subject_code_dict_class_10
            if (class_std == "10")
            else subject_code_dict_class_12
        )
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
        for grade, weightage in grades_list:
            count = grades_dict.get(grade, 0)
            pi_data.append([grade, count])
            pi_value += weightage * count

        pi_value /= len(subject_list) * 8
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
