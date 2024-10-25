import csv

def native_csv_read(filepath: str) -> list[tuple]:
    with open(filepath, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        data = []
        for idx, line in enumerate(reader):
            data.append((idx, *line))
        return data

def native_csv_write(filepath: str, headers: list, rows: list[tuple]):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row[1:])


if __name__ == "__main__":
    # test de la fonction
    data = native_csv_read("example.csv")
    print(data)
    headers = ["Index", "Column1", "Column2"]
    native_csv_write("output.csv", headers, data)


