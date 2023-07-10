def get_csv_names():
    with open('Sources/commonNames.csv') as f_names:
        import csv
        f_reader = csv.reader(f_names, delimiter=',')
        line = 0
        names = list()  # list of all names to be added
        for row in f_reader:
            if line == 0:  # if the line is header
                # print(f'Header: {", ".join(row)}')
                line += 1
            else:
                # print(row[0])
                names.append(row[0])  # add the first value (the name) to the list of names
                line += 1
    uniq_names = set(names)
    return uniq_names


if __name__ == "__main__":
    print(get_csv_names())
    print(len(get_csv_names()))  # 447055
    print(type(get_csv_names()))