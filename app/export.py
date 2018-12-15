import os
import json
import csv
from datetime import date
from ansimarkup import ansiprint as print
from openpyxl import Workbook


def export_date_medici(tip, lista_date_medici):
    nume_fisier = f"export/export_{date.today()}.{tip}"
    os.makedirs(os.path.dirname(nume_fisier), exist_ok=True)

    if tip == "json":
        with open(nume_fisier, "w") as outfile:
            json.dump(lista_date_medici, outfile)

    if tip == "csv":
        with open(nume_fisier, "w", newline="") as csvfile:
            csv_writer = csv.writer(
                csvfile, dialect="excel", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            for medic in lista_date_medici:
                csv_writer.writerow([medic["cuim"], medic["nume"], medic["prenume"]])

    if tip == "xlsx":
        book = Workbook()
        sheet = book.active

        first_row = ("index", "cuim", "nume", "prenume")

        sheet.append(first_row)
        

        for index, medic in enumerate(lista_date_medici):
            row = (index + 1, medic["cuim"], medic["nume"], medic["prenume"])
            sheet.append(row)

        book.save(nume_fisier)

    print(f"<green>** Export finalizat.</green> Fisier: =>  {nume_fisier}")

