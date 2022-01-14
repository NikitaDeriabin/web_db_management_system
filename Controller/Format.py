def table_to_json(table):
    formatted_table = dict()
    formatted_table["records"] = []
    for row in table.rows:
        row_dict = dict()

        for cell in row.cells:
            row_dict[cell.name_attr] = cell.val

        formatted_table["records"].append(row_dict)

    return formatted_table
