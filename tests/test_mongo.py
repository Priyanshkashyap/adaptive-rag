from src.db.mongodb import get_database


def main():

    db = get_database()

    print(db.name)


if __name__ == "__main__":
    main()