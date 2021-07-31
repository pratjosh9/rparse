def get_student_details(student_split, marks_split):
    roll_no = student_split[0]
    gender = student_split[1]
    name = []
    idx = 2
    while not student_split[idx].isnumeric():
        if student_split[idx] != " ":
            name.append(student_split[idx])
        idx += 1
    name = " ".join(name)

    subjects_list = []
    int_sb_grd = []
    misc_list = []
    result = None

    for i in range(idx, len(student_split)):
        if student_split[i] in [" ", ""]:
            continue

        if student_split[i].isnumeric():
            code = student_split[i]
            subjects_list.append([code])
        else:
            if len(int_sb_grd) < 3 and student_split[""]:
                int_sb_grd.append(student_split[i])
            elif result is None:
                result = student_split[i]
            else:
                misc_list.append(student_split[i])

    for i in range(len(marks_split)):
        idx = i // 2
        subjects_list[idx].append(marks_split[i])

    # print(roll_no, gender, name, subjects_list, int_sb_grd, result, misc_list)
    return Student(roll_no, gender, name, subjects_list, result, misc_list)


def parse_result_file(filename):
    students_list = []

    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        i = 0
        while i < len(lines):
            clean_line = lines[i]
            splits = clean_line.split(" ")
            i += 1
            if not splits[0].isnumeric():
                continue

            splits = list(filter(lambda x: x != "" and x != " ", splits))
            next_line = lines[i]
            split_2 = next_line.split(" ")
            split_2 = list(filter(lambda x: x != "" and x != " ", split_2))
            students_list.append(get_student_details(splits, split_2))
            i += 1

    print("Number of students ", len(students_list))
    workbook = xlsxwriter.Workbook("Example.xlsx")

    for sub_code in distinct_subjects:
        get_subject_wise_list(students_list, sub_code, workbook)

    write_section_list(students_list, workbook)
    workbook.close()


def write_section_list(students_list):
    distinct_sub_combo_dict = {}

    for student in students_list:
        name = student.name
        subjects_dict = student.subjects_dict
        total_marks = student.total_marks

        sorted_subject_list = sorted(subjects_dict.keys())
        subject_list_hash = "_".join(sorted_subject_list)
        if subject_list_hash not in distinct_sub_combo_dict:
            distinct_sub_combo_dict[subject_list_hash] = []

        data = [name]
        for subject in sorted_subject_list:
            data.extend([subjects_dict[subject][0], subjects_dict[subject][1]])
        data.append(total_marks)

        distinct_sub_combo_dict[subject_list_hash].append(data)

    for subject_combo, subject_data in distinct_sub_combo_dict.items():
        fields = ["Student Name"]
        subjects_list = subject_combo.split("_")

        for subject_code in subjects_list:
            marks_field = "{0}_Marks".format(subject_code)
            grade_field = "{0}_Grade".format(subject_code)
            fields.extend([marks_field, grade_field])

        fields.append("Total Marks")

        subject_names = "_".join(
            [subject_code_dict[subject_code] for subject_code in subjects_list]
        )
        filename = "{0}.csv".format(subject_names)
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(subject_data)
