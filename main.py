# Module for testing
import csv_creator


def main():
    try:
        fsrc, ftarg = csv_creator.from_txt('src', 'targ')
    except ValueError:
        print(ValueError)
        exit(-1)
    except FileNotFoundError:
        print(FileNotFoundError)
        exit(-1)
    else:
        print(f"Result:\nCSV file '{fsrc}' was successfully written with data from TXT file '{ftarg}'.")
    # Reading for control
    csv_creator.read_csv('targ', show=True)


if __name__ == '__main__':
    main()
else:
    print("Error: no entering point!")
    exit(-1)
