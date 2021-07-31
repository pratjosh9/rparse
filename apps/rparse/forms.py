from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_file_size(value):
    filesize = value.size
    max_file_size = 100000  # max_file_size = 10 KB
    if filesize > max_file_size:
        raise ValidationError("The maximum file size that can be uploaded is 100KB")

    return value


class UploadFileForm(forms.Form):
    CHOICES = (("10", "Class 10"), ("12", "Class 12"))

    class_std = forms.ChoiceField(label="Class", choices=CHOICES)
    file = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["txt"],
                message="Only .txt files are supported",
                code=406,
            ),
            validate_file_size,
        ]
    )
