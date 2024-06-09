from django.http import HttpResponseBadRequest
from django.shortcuts import render

from .forms import UploadFileForm, ICSEUploadFileForm
from .utils import parse_form_file, parse_icse_form_file

def cbse_parser(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            class_std = request.POST.get("class_std", None)
            if class_std not in ["10", "12"]:
                response = HttpResponseBadRequest(
                    f"<h1>Bad Request</h1><p>Invalid Class {class_std} Entered</p>"
                )
            response = parse_form_file(request.FILES["file"], class_std)
            return response
    else:
        form = UploadFileForm()
    return render(request, "rparse/cbse.html", {"form": form})

def icse_parser(request):
    if request.method == "POST":
        form = ICSEUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            class_std = request.POST.get("class_std", None)
            if class_std not in ["10", "12"]:
                response = HttpResponseBadRequest(
                    f"<h1>Bad Request</h1><p>Invalid Class {class_std} Entered</p>"
                )
            response = parse_icse_form_file(request.FILES["file"], class_std)
            return response
    else:
        form = ICSEUploadFileForm()
    return render(request, "rparse/icse.html", {"form": form})

def home_page(request):
    return render(request, "rparse/home.html")