import json
import sys

import xlrd


ERROR_CTYPE = 5
TRADE_REMEDY_FOOTNOTE = '₁'
SUSPENSION_FOOTNOTE = '₂'

def excel_to_json(input_file: str, output_file: str, sheet_name: str = "Sheet1"):
    workbook = xlrd.open_workbook(input_file)
    worksheet = workbook.sheet_by_name(sheet_name)

    data = []

    for row_number, row in enumerate(worksheet.get_rows()):
        if row_number == 0:
            continue

        if any(item.ctype == ERROR_CTYPE for item in row):
            print(f"Failed row with code {row[1].value}")
            continue

        if (type(row[1].value) is not str):
            print(f"Row {row_number}: CC is not a string, is {type(row[1].value)}")
            continue

        if ((row[0].value == 'CN8' and len(row[1].value) != 8) or
            (row[0].value == 'CN10' and len(row[1].value) != 10) or
            not (row[0].value == 'CN10' or row[0].value == 'CN8')):
           print(f"Row {row_number}: code '{row[1].value}' has incorrect CC length")
           continue

        data.append(
            {
                "commodity": row[1].value,
                "description": row[2].value,
                "cet_duty_rate": row[3].value,
                "ukgt_duty_rate": row[4].value,
                "change": row[5].value.replace(TRADE_REMEDY_FOOTNOTE, '').replace(SUSPENSION_FOOTNOTE, ''),
                "trade_remedy": (TRADE_REMEDY_FOOTNOTE in row[5].value),
                "suspension": (SUSPENSION_FOOTNOTE in row[5].value)
            }
        )

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    excel_to_json(sys.argv[1], sys.argv[2])
