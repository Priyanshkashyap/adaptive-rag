from src.embeddings.ollama_embeddings import (get_embeddings,)

def main() -> None:

    embeddings = get_embeddings()
    vector = embeddings.embed_query("What is React?")
    print(f"Vector length: {len(vector)}")
    print(vector[:10])

if __name__ == "__main__":
    main()