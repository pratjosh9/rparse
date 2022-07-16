import uuid
import xlsxwriter

from .reader import ResultReader
from .writer import ResultWriter


class ResultToExcelParser(object):
    def __init__(self, class_std):
        self.class_std = class_std
        self.students_list = None
        self.distinct_subjects = None
        # List is a pair of (Name, Workbook Object)
        self.workbook_list = [None, None]

    def _read_result(self, lines):
        reader = ResultReader(lines)
        self.students_list = reader.get_students_list()
        self.distinct_subjects = reader.get_distinct_subjects()

    def read_result_file(self, result_filename):
        with open(result_filename) as file:
            lines = file.readlines()
        self._read_result(lines)

    def read_result_from_server_file(self, file_object):
        lines = list(map(lambda x: x.decode("utf-8"), file_object.readlines()))
        self._read_result(lines)

    def write_result_workbook(self, response_io_object=None):
        self.workbook_list[0] = f"{uuid.uuid1().hex}.xlsx"
        self.workbook_list[1] = (
            xlsxwriter.Workbook(response_io_object)
            if response_io_object
            else xlsxwriter.Workbook(self.workbook_list[0])
        )
        writer = ResultWriter(
            self.students_list,
            self.workbook_list[1],
            self.distinct_subjects,
            self.class_std,
        )
        writer.write_result()

    def parse_result_from_filename(self, result_filename):
        self.read_result_file(result_filename)
        self.write_result_workbook()

    def parse_result_from_server_file(self, file_object, response_io_object):
        self.read_result_from_server_file(file_object)
        self.write_result_workbook(response_io_object)

    def get_workbook_list(self):
        return self.workbook_list

    def get_workbook_name(self):
        return self.workbook_list[0]
