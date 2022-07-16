import time

from result_parser.parser import ResultToExcelParser

if __name__ == "__main__":
    FILENAME = "84055.txt"
    CLASS_STD = "10"

    start_time = time.time()
    result_parser = ResultToExcelParser(CLASS_STD)
    result_parser.parse_result_from_filename(FILENAME)
    workbook_name = result_parser.get_workbook_name()

    print(f"Workbook {workbook_name} written successfully")
    print(f"Time Taken {time.time()-start_time}")
