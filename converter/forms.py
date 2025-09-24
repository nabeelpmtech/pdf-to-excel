from django import forms

class UploadPDFForm(forms.Form):
    pdf_file = forms.FileField(label="Upload PDF", help_text="Upload a PDF containing tables")
