import json

from query import ask

QUESTIONS = [
    "Is it safe to live alone in southside Berkeley?",
    "When should I start looking for an apartment for the next school year?",
    "Which landlords or property management companies do students say to avoid?",
    "How much should I expect to pay in rent near campus?",
    "What is the best dining hall on campus?",
]


def main():
    results = []
    for q in QUESTIONS:
        print("=" * 70)
        print(f"Q: {q}")
        result = ask(q)
        print(result["answer"])
        print("Sources:", ", ".join(result["sources"]) or "none")
        print("Retrieved chunks:")
        for h in result["hits"]:
            print(f"  [{h['distance']:.3f}] {h['source']}: {h['text'][:120]!r}")
        results.append({
            "question": q,
            "answer": result["answer"],
            "sources": result["sources"],
            "chunks": [
                {"source": h["source"], "distance": h["distance"], "text": h["text"]}
                for h in result["hits"]
            ],
        })
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nsaved eval_results.json")


if __name__ == "__main__":
    main()
