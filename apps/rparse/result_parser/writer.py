from .constants import GRADES_TO_PI_MAP
from .utils import write_worksheet, get_subject_code_dict_from_class_std


class ResultWriter(object):
    """
    Dumb writer class takes the list of students and writes the result directly
    Has minimum logic for easy extensibility
    """

    def parse_student_info(self):
        if len(self.students_list) == 0:
            raise ValueError("No Students Found")

        for sub_code in self.distinct_subjects:
            self.get_subject_wise_list(sub_code)

        self.write_school_pi()
        self.write_section_list()

    def __init__(self, students_list, workbook, distinct_subjects, class_std):
        self.subject_code_dict = get_subject_code_dict_from_class_std(class_std)
        self.class_std = class_std
        self.grades_dict = {}
        self.workbook = workbook
        self.distinct_subjects = distinct_subjects
        self.students_list = students_list

    def write_result(self):
        self.parse_student_info()
        self.workbook.close()

    def get_section_data(self, subject_list, mandatory_subject, section_name):
        fields = ["Student Name"]
        for subject_code in subject_list:
            subject_name = self.subject_code_dict.get(
                subject_code, f"Subject Code - {subject_code}"
            )
            fields.extend(
                [
                    f"{subject_name}_marks",
                    f"{subject_name}_grade",
                ]
            )
        fields.extend(
            [f"Total Marks{len(subject_list)*100}", "Result", "Compartment Data"]
        )

        section_data = []

        for student in self.students_list:
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
            self.get_section_data(self.distinct_subjects, "086", "Class X")

    def write_school_pi(self):
        fields = ["Grade", "Frequency"]

        pi_data, pi_value = [], 0
        frequency = 0
        for grade, weightage in GRADES_TO_PI_MAP:
            count = self.grades_dict.get(grade, 0)
            frequency += count
            pi_data.append([grade, count])
            pi_value += weightage * count

        if frequency:
            pi_value /= frequency * 8

        pi_data.append(["pi", pi_value * 100])
        worksheet_name = "School PI"
        write_worksheet(self.workbook, worksheet_name, fields, pi_data)

    def write_pi_list(self, subject_list, sub_code):
        grades_dict = {}
        for data in subject_list:
            grade = data[3]
            if grade not in grades_dict:
                grades_dict[grade] = 0
            grades_dict[grade] += 1

        fields = ["Grade", "Frequency"]

        pi_data, pi_value = [], 0
        frequency = 0
        for grade, weightage in GRADES_TO_PI_MAP:
            count = grades_dict.get(grade, 0)
            frequency += count
            if grade not in self.grades_dict:
                self.grades_dict[grade] = 0
            self.grades_dict[grade] += count
            pi_data.append([grade, count])
            pi_value += weightage * count

        if frequency:
            pi_value /= frequency * 8

        pi_data.append(["pi", pi_value * 100])
        subject_name = self.subject_code_dict.get(
            sub_code, f"Subject Code - {sub_code}"
        )
        worksheet_name = f"{subject_name}_PI"
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

            sub_marks = int(sub_marks) if sub_marks != "AB" else sub_marks
            subject_data = [student.roll_no, student.name, sub_marks, sub_grade]
            subject_list.append(subject_data)

        subject_name = self.subject_code_dict.get(
            sub_code, f"Subject Code - {sub_code}"
        )
        write_worksheet(
            self.workbook,
            subject_name,
            subject_list_fields,
            subject_list,
        )
        self.write_pi_list(subject_list, sub_code)
