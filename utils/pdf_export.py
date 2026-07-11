from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def export_pdf(df):

    filename = "Sales_Report.pdf"

    pdf = SimpleDocTemplate(filename)

    data = [df.columns.tolist()]

    for row in df.values.tolist():
        data.append(row)

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.grey),

        ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    pdf.build([table])

    return filename