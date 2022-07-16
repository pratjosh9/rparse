from django.http import HttpResponseBadRequest
from django.shortcuts import render

from .forms import UploadFileForm
from .utils import parse_form_file


def upload_file(request):
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
    return render(request, "rparse/form.html", {"form": form})
