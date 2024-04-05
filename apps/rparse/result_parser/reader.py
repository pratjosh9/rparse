from .student import Student
from .utils import clean_line


class ResultReader(object):
    """
    Dumb Reader Class to support reading from a file of specific format
    Can be extended to multiple classes later
    """

    def __init__(self, lines):
        self.distinct_subjects = set()
        self.students_list = self.parse_lines(lines)

    def _sanitize_subject_code(self, sub_code):
        if len(sub_code) >= 3:
            return sub_code
        diff = 3 - len(sub_code)
        return "0" * diff + sub_code

    def get_student(self, student_line, marks_line, distinct_subjects, is_absent):
        student_split = clean_line(student_line)
        marks_split = clean_line(marks_line)
        student_data = {"Roll No": student_split[0], "Gender": student_split[1]}

        name_list = []
        idx = 2
        while idx < len(student_split) and not student_split[idx].isnumeric():
            name_list.append(student_split[idx])
            idx += 1
        student_data["Name"] = " ".join(name_list)

        subject_idx = 1
        while idx < len(student_split) and student_split[idx].isnumeric():
            subject_key = f"Subject {subject_idx}"
            sub_code = self._sanitize_subject_code(student_split[idx])
            distinct_subjects.add(sub_code)
            student_data[subject_key] = [sub_code]
            if is_absent:
                student_data[subject_key].extend(['000', "E"])
            idx += 1
            subject_idx += 1

        while idx < len(student_split) and len(student_split[idx]) <= 2:
            idx += 1

        student_data["Result"] = student_split[idx]

        student_data["Misc Data"] = (
            "" if idx + 1 == len(student_split) else " ".join(student_split[idx + 1 :])
        )

        if len(marks_split) % 2 == 1:
            # Class X results have an additional column of Total Marks
            student_data["Total"] = marks_split.pop(-1)

        if not is_absent:
            for idx in range(len(marks_split)):
                subject_idx = idx // 2 + 1
                subject_key = f"Subject {subject_idx}"
                student_data[subject_key].append(marks_split[idx])
        return Student(student_data)

    def parse_lines(self, lines):
        students_list = []
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            idx += 1

            line = line.replace("\t", " ")

            if not line:
                continue

            if not line[0].isnumeric():
                continue

            mark_line = ""
            is_absent = "ABST" in line
            if not is_absent:
                mark_line = lines[idx]
                mark_line = mark_line.replace("\t", " ")

            students_list.append(
                self.get_student(line, mark_line, self.distinct_subjects, is_absent)
            )
            idx += 1
        return students_list

    def get_students_list(self):
        return self.students_list

    def get_distinct_subjects(self):
        return self.distinct_subjects
