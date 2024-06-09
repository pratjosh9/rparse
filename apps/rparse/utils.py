import io
import logging

from django.http import HttpResponseBadRequest, HttpResponse

from .result_parser.parser import ResultToExcelParser
from .icse_result_parser.parser import ResultToExcelParser as ICSEResultParser


def parse_form_file(server_file, class_std):
    try:
        response_io_object = io.BytesIO()
        result_parser = ResultToExcelParser(class_std)
        result_parser.parse_result_from_server_file(server_file, response_io_object)
        workbook_name = result_parser.get_workbook_name()
        response_io_object.seek(0)
    except Exception as e:
        logging.exception(e)
        response = HttpResponseBadRequest(f"<h1>Bad Request</h1><p>{e}</p>")
    else:
        filename = f"result_{workbook_name}"
        response = HttpResponse(
            response_io_object,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

    return response

def parse_icse_form_file(server_file, class_std):
    try:
        response_io_object = io.BytesIO()
        result_parser = ICSEResultParser(class_std)
        result_parser.parse_result_from_server_file(server_file, response_io_object)
        workbook_name = result_parser.get_workbook_name()
        response_io_object.seek(0)
    except Exception as e:
        logging.exception(e)
        response = HttpResponseBadRequest(f"<h1>Bad Request</h1><p>{e}</p>")
    else:
        filename = f"result_{workbook_name}"
        response = HttpResponse(
            response_io_object,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
