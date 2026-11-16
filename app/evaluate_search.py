
import json
from pathlib import Path

from app.vectorstore import semantic_search

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"

OUTPUT_FILE = BASE_DIR / "eval" / "search_results.md"

def evaluate_search():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(file)

    questions = [
        item for item in questions
        if item.get("id") in range(1, 11)
    ]

    lines = [
        "# StartupSetu Semantic Search Evaluation",
        "",
        "Embedding model: all-MiniLM-L6-v2",
        "Vector database: ChromaDB",
        "Top K: 3",
        ""
    ]

    for item in questions:

        question = item["question"]

        print("\nSearching:", question)

        results = semantic_search(
            query=question,
            top_k=3
        )

        lines.append(f"## Question {item['id']}")
        lines.append("")
        lines.append(f"**Question:** {question}")
        lines.append("")
        lines.append(
            f"**Answerable from dataset:** "
            f"{item.get('answerable_from_dataset', 'Not specified')}"
        )
        lines.append("")
        
        if results:

            lines.append("| Rank | Document | Record ID | Score |")
            lines.append("|---|---|---|---|")

            for rank, result in enumerate(results, start=1):

                metadata = result["metadata"]

                title = metadata.get("title", "Unknown")
                record_id = metadata.get("record_id", "Unknown")
                score = result["similarity_score"]

                lines.append(
                    f"| {rank} | {title} | "
                    f"{record_id} | {score} |"
                )

        else:
            lines.append("No search results found.")

        lines.append("")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nEvaluation completed!")
    print("Results saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    evaluate_search()