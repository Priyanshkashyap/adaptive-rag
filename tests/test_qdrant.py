from src.db.qdrant import get_qdrant_client


def main():

    client = get_qdrant_client()

    print(client.get_collections())


if __name__ == "__main__":
    main()