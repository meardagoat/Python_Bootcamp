def display_message():
    print("display_message appelé depuis le module other")


def main():
    print("main appelé depuis le module other")
    display_message()


if __name__ == "__main__":
    main()