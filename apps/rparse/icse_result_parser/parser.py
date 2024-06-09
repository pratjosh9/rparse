import pymupdf
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

    def parse_result_from_server_file(self, file_object, response_io_object=None):
        pdf_doc = pymupdf.open(file_object.name, bytearray(file_object.read()))
        reader = ResultReader()
        students = []
        for page in pdf_doc:
            text = page.get_text(sort=True)
            # Discard pages that do not have the results table
            if "UNIQUE ID" not in text:
                continue

            # Discard lines leading upto UNIQUE ID
            find_idx = text.find("UNIQUE ID")
            # Discard lines containing Run at DD/MM/YYYY
            run_at_idx = text.find("Run at")
            text = text[find_idx:run_at_idx]
            
            students.extend(reader.read_page(text))

        self.workbook_list[0] = f"{self.class_std}_result_{uuid.uuid1().hex}.xlsx"
        self.workbook_list[1] = (
            xlsxwriter.Workbook(response_io_object)
            if response_io_object
            else xlsxwriter.Workbook(self.workbook_list[0])
        )
        
        writer = ResultWriter(
            students,
            self.workbook_list[1],
            reader.get_major_subjects(),
            reader.get_component_subjects(),
            self.class_std
        )
        writer.write_result()      

    def get_workbook_name(self):
        return self.workbook_list[0]
      
        