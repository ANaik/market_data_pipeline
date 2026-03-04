from pyalex import Works


def main() -> None:
    query = "artificial intelligence"

    works = Works().search(query).get(per_page=5)

    print("Top 5 AI-related papers from OpenAlex:\n")
    for i, work in enumerate(works, start=1):
        title = work.get("display_name") or "No title available"
        print(f"{i}. {title}")


if __name__ == "__main__":
    main()

