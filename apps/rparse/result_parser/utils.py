from .constants import subject_code_dict_class_12, subject_code_dict_class_10


def clean_line(line):
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), line.split(" "))))


def write_worksheet(workbook, worksheet_name, fields, data_list):
    worksheet = workbook.add_worksheet(worksheet_name)
    worksheet.write_row(0, 0, fields)
    for idx, data in enumerate(data_list):
        worksheet.write_row(idx + 1, 0, data)


def get_subject_code_dict_from_class_std(class_std):
    if class_std == "12":
        return subject_code_dict_class_12

    if class_std == "10":
        return subject_code_dict_class_10

    raise ValueError("Invalid class_std provided")
