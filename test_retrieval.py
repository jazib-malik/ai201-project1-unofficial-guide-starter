from query import retrieve

QUERIES = [
    "Is it safe to live alone in southside?",
    "When should I start looking for an apartment for next year?",
    "Which landlords or property companies should I avoid?",
]


def main():
    for q in QUERIES:
        print("=" * 70)
        print(f"Query: {q}")
        for hit in retrieve(q):
            print(f"\n[distance {hit['distance']:.3f}] from {hit['source']}")
            preview = hit["text"][:300].replace("\n", " ")
            print(f"  {preview}")
        print()


if __name__ == "__main__":
    main()
