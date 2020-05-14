import json
import sys

import xlrd


ERROR_CTYPE = 5


def clean_tariff_rate(value):
    if isinstance(value, float):
        value = f"{round(value * 100, 2)}%"

    return value


def excel_to_json(input_file: str, output_file: str, sheet_name: str = "Sheet1"):
    workbook = xlrd.open_workbook(input_file)
    worksheet = workbook.sheet_by_name(sheet_name)

    data = []

    for row_number, row in enumerate(worksheet.get_rows()):
        if row_number == 0:
            continue

        if any(item.ctype == ERROR_CTYPE for item in row):
            print(f"Row {row_number}: Failed row with code {row[0].value}")
            continue

        if not isinstance(row[1].value, str):
            print(f"Row {row_number}: CC is not a string, is {type(row[1].value)}")
            continue

        if row[2].value and (
            len(row[0].value) != 10 or row[0].value != row[1].value + row[2].value
        ):
            print(f"Row {row_number}: Code '{row[0].value}' is malformed.")
            continue

        if row[7].value is None and row[8].value is not None:
            print(f"Row {row_number}: Dumping margin without trade remedy.")
            continue

        data.append(
            {
                "commodity": row[0].value,
                "description": row[3].value,
                "cet_duty_rate": clean_tariff_rate(row[4].value),
                "ukgt_duty_rate": clean_tariff_rate(row[5].value),
                "change": row[6].value,
                "trade_remedy_applies": row[7].value is not None and row[7].value != "",
                "dumping_margin_applies": row[8].value == "TRUE" or row[8].value == 1,
                "suspension_applies": row[10].value is not None and row[10].value != "",
                "eps_applies": row[11].value is not None and row[11].value != "",
                "meursing_applies": row[13].value is not None and row[13].value != "",
            }
        )

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    excel_to_json(sys.argv[1], sys.argv[2])
