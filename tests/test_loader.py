from src.rag.document_loader import (
    load_txt_document,
)
from src.rag.text_splitter import (
    split_documents,
)


def main():

    docs = load_txt_document(
        "sample.txt",
    )

    chunks = split_documents(
        docs,
    )

    print(
        f"Total Chunks: {len(chunks)}"
    )

    for index, chunk in enumerate( # You use enumerate() when you need both:the item itself,its position in the list
        chunks,
    ):
        print(
            f"\nChunk {index + 1}"
        )
        print(
            chunk.page_content[:100]
        )


if __name__ == "__main__":
    main()