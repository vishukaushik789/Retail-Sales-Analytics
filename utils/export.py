from openpyxl import Workbook


def export_excel(df):

    wb = Workbook()

    ws = wb.active

    ws.title = "Sales Report"

    ws.append(df.columns.tolist())

    for row in df.values.tolist():
        ws.append(row)

    filename = "Sales_Report.xlsx"

    wb.save(filename)

    return filename