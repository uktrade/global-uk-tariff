import json
import sys

import xlrd


ERROR_CTYPE = 5


def excel_to_json(input_file: str, output_file: str, sheet_name: str = "Sheet1"):
    workbook = xlrd.open_workbook(input_file)
    worksheet = workbook.sheet_by_name(sheet_name)

    data = []

    for row_number, row in enumerate(worksheet.get_rows()):
        if any(item.ctype == ERROR_CTYPE for item in row):
            print(f"Failed row with code {row[0].value}")
            continue
        data.append(
            {
                "commodity": row[0].value,
                "description": row[2].value,
                "cet_duty_rate": row[3].value,
                "ukgt_duty_rate": row[4].value,
                "change": row[5].value,
            }
        )

    with open(output_file, "w") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    excel_to_json(sys.argv[1], sys.argv[2])
