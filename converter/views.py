import os

# Set JAVA_HOME to the real JDK path
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"

# Add Java bin to PATH so tabula can find java.exe
os.environ["PATH"] += os.pathsep + os.path.join(os.environ["JAVA_HOME"], "bin")

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import tabula
import os
from .forms import UploadPDFForm
from django.conf import settings
from django.shortcuts import render,redirect

def upload_view(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
            with open(pdf_path, 'wb+') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Extract tables from PDF
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

            # Save tables to Excel
            excel_file = os.path.join(settings.MEDIA_ROOT, pdf_file.name.replace('.pdf', '.xlsx'))
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                for idx, table in enumerate(tables):
                    table.to_excel(writer, sheet_name=f'Table{idx+1}', index=False)

            # Provide download link
            #return HttpResponse(f"Excel file created: <a href='/media/{os.path.basename(excel_file)}'>Download</a>")
            file_name = os.path.basename(excel_file)
            return redirect(f"/result/?file_name={file_name}")

    else:
        form = UploadPDFForm()

    return render(request, 'converter/upload.html', {'form': form})

def convert_pdf(request):
    # Get the file_name from the query string
    file_name = request.GET.get('file_name')

    # Build the file URL for the template
    file_url = f"/media/{file_name}" if file_name else None

    return render(request, "converter/result.html", {
        "file_url": file_url
    })




