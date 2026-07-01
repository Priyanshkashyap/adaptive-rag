from src.tools.search import get_tavily_client


def main():

    client = get_tavily_client()

    response = client.search(
        "Latest AI news"
    )

    print(response)


if __name__ == "__main__":
    main()