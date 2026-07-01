from src.llms.ollama_client import get_llm

def main():

    llm = get_llm()

    response = llm.invoke( # asks model
        "Say hello in one sentence."
    )

    print(response.content)


if __name__ == "__main__":
    main()