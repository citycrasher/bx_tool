import csv
from django.template.loader import get_template
from xhtml2pdf import pisa # for pdf
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO

def render_to_pdf(template_src, context_dict={}):
    template = get_template('utils/content_test_table_duplicate.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_csv(context):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{movie_name}.csv"'.format(movie_name=context["movie_obj"].movie_name)

    # Create a CSV writer object
    writer = csv.writer(response)
    for data in context["datas"]:
        writer.writerow([data.time_stamp, data.report_id, data.request_id, data.original_type, data.report_url, data.status])

    return response
def generate_pdf(context):
    template = get_template('export/exportPDF.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_excel(context):
    # Create a new workbook and a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    # Write the header row
    ws.append(['Column 1', 'Column 2', 'Column 3'])

    # Write some data rows
    ws.append(['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'])
    ws.append(['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3'])
    ws.append(['Row 3 Col 1', 'Row 3 Col 2', 'Row 3 Col 3'])

    # Set the response content type to Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

