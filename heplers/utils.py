# -*- coding:utf-8 -*-
from flask import make_response


def export_excel(filename, office):
    out_put = office.getvalue()
    output = make_response(out_put)
    output.headers[
        "Content-Disposition"] = "attachment; filename={0}.xlsx".format(
        filename)
    output.headers[
        "Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return output


def export_pdf(filename, office):
    out_put = office.getvalue()
    output = make_response(out_put)
    output.headers[
        "Content-Disposition"] = "attachment; filename={0}.pdf".format(
        filename)
    output.headers[
        "Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.pdf"
    return output
