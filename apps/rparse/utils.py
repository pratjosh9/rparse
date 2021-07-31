import io
import logging
import uuid
import time
import xlsxwriter

from django.http import HttpResponseBadRequest, HttpResponse, FileResponse

from .parser import ResultParser


def parse_result_file(filename, class_std):
    workbook_name = f"{uuid.uuid4().hex}.xlsx"
    workbook = xlsxwriter.Workbook(workbook_name)

    with open(filename) as f:
        lines = f.readlines()
        parse_result(lines, workbook, class_std)


def parse_form_file(f, class_std):
    response_io_object = io.BytesIO()
    workbook = xlsxwriter.Workbook(response_io_object)

    try:
        lines = list(map(lambda x: x.decode("utf-8"), f.readlines()))
        parse_result(lines, workbook, class_std)
        response_io_object.seek(0)
    except Exception as e:
        # logging.exception(e)
        response = HttpResponseBadRequest(f"<h1>Bad Request</h1><p>{e}</p>")
    else:
        filename = "result.xlsx"
        response = HttpResponse(
            response_io_object,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def parse_result(lines, workbook, class_std):
    rp = ResultParser(lines, workbook, class_std)


if __name__ == "__main__":
    start_time = time.time()
    filename = "res1.txt"
    parse_result_file(filename, "12")
    print(f"Time Taken {time.time()-start_time}")
