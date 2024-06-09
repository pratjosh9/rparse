
def write_worksheet(workbook, worksheet_name, fields, data_list):
    worksheet = workbook.add_worksheet(worksheet_name)
    worksheet.write_row(0, 0, fields)
    for idx, data in enumerate(data_list):
        worksheet.write_row(idx + 1, 0, data)


class ResultWriter(object):
    """
    Dumb writer class takes the list of students and writes the result directly
    Has minimum logic for easy extensibility
    """

    def parse_student_info(self):
        if len(self.students_list) == 0:
            raise ValueError("No Students Found")

        for sub_code in self.major_subjects:
            self.get_subject_wise_list(sub_code)

        self.get_school_result()

    def __init__(self, students_list, workbook, major_subjects, component_subjects, class_std):
        self.grades_dict = {}
        self.major_subjects = major_subjects
        self.component_subjects = component_subjects
        self.students_list = students_list
        self.workbook = workbook
        self.class_std = class_std

    def get_school_result(self):
        school_list_fields = ["Unique Id 1", "Unique Id 2", "Name"]

        # List subjects starting with english
        school_list_fields.extend(["ENG"])

        # inverted map for getting the index of the subject in the header
        header_idx = {"ENG": 0}
        num_subject_columns = 1

        for subject in self.major_subjects:
            if subject == "ENG":
                continue

            school_list_fields.append(subject)
            header_idx[subject] = num_subject_columns
            num_subject_columns += 1

        # Best total
        school_list_fields.extend(["Result", "ENG + Best 4" if self.class_std == "10" else "ENG + Best 3", "%"])        
        
        school_list = []
        for student in self.students_list:
            student_data = [student.unique_id_1, student.unique_id_2, student.name]
            # fill the data with empty string to initialize the list
            subject_data = ["" for i in range(num_subject_columns)]

            # Add the marks for student to this list
            marks_list = []
            for subject in student.subjects:
                if subject not in self.major_subjects:
                    continue

                marks = student.subjects[subject]["marks"]
                subject_data[header_idx[subject]] = int(marks) if marks.isnumeric() else 0
                if subject != "ENG":
                    marks_list.append(subject_data[header_idx[subject]])
            
            marks_list.sort(reverse=True)
            best_marks = subject_data[header_idx["ENG"]]
            percentage = 0
            if self.class_std == "10":
                best_marks += sum(marks_list[:4])
                percentage = best_marks / 5
            else:
                best_marks += sum(marks_list[:3])
                percentage = best_marks / 4

            student_data.extend(subject_data)
            student_data.extend([student.result, best_marks, f'{percentage:.4g}'])
            school_list.append(student_data)

        write_worksheet(
            self.workbook,
            "School Results",
            school_list_fields,
            school_list,
        )
        
    def write_result(self):
        self.parse_student_info()
        self.workbook.close()

    def get_subject_wise_list(self, sub_code):
        subject_list_fields = ["Unique Id 1", "Unique Id 2", "Name", f"{sub_code} - Marks", f"{sub_code} - Grade"]
        
        has_component_subjects = sub_code in self.component_subjects

        if has_component_subjects:
            subject_list_fields.extend([f"{x} - Marks" for x in self.component_subjects[sub_code]])

        subject_list = []
        for student in self.students_list:

            if sub_code not in student.subjects:
                continue

            sub_marks, sub_grade = (
                student.subjects[sub_code]["marks"],
                student.subjects[sub_code]["grade"],
            )

            sub_marks = int(sub_marks) if sub_marks.isnumeric() else sub_marks
            subject_data = [student.unique_id_1, student.unique_id_2, student.name, sub_marks, sub_grade]

            if has_component_subjects and "components" in student.subjects[sub_code]:
                for component_subject in self.component_subjects[sub_code]:
                    comp_sub_marks = student.subjects[sub_code]["components"][component_subject]
                    subject_data.append(int(comp_sub_marks) if comp_sub_marks.isnumeric() else comp_sub_marks)

            subject_list.append(subject_data)

        write_worksheet(
            self.workbook,
            sub_code,
            subject_list_fields,
            subject_list,
        )
