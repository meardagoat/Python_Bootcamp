def read_one_line(filename: str) -> str:
    with open(filename, "r") as file:
        return file.readline()


def write_text(filename: str, text: str):
    with open(filename, "w") as file:
        file.write(text)


def copy_characters(input_file: str, output_file: str, nb: int):
    try:
        with open(input_file, 'r') as infile:
            content = infile.read(nb)
        with open(output_file, 'a') as outfile:
            outfile.write(content + '\n' if content or nb == 0 else '')
    except Exception as e:
        print(f"An error occurred: {e}")


def read_all_lines(filename: str) -> (list[str], list[str]):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines, lines[::2]


def write_text_better(filename: str, text: str):
    with open(filename, "w") as file:
        file.write(text)


def copy_characters_better(input_file: str, output_file: str, nb: int):
    with open(input_file, "r") as infile, open(output_file, "a") as outfile:
        outfile.write("\n" + infile.read(nb))


if __name__ == "__main__":
    # test des fonctions
    print(read_one_line("example.txt"))
    write_text("output.txt", "Hello, World!")
    copy_characters("input.txt", "output.txt", 10)
    all_lines, even_lines = read_all_lines("example.txt")
    print(all_lines)
    print(even_lines)
    write_text_better("better_output.txt", "Better Hello, World!")
    copy_characters_better("input.txt", "better_output.txt", 10)