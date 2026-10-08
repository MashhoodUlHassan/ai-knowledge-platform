from datasets import Dataset
from ragas import evaluate

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

from evaluation.dataset import EVALUATION_DATASET
from app.agents.graph import agent_graph, llm


def main():
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    print("\n===== Starting RAGAS Evaluation =====\n")

    for index, item in enumerate(EVALUATION_DATASET, start=1):
        question = item["question"]

        print(
            f"[{index}/{len(EVALUATION_DATASET)}] "
            f"Evaluating: {question}"
        )

        try:
            result = agent_graph.invoke(
                {
                    "query": question,
                    "retrieved_context": [],
                    "answer": "",
                }
            )

            retrieved_context = result["retrieved_context"]

            questions.append(question)
            answers.append(result["answer"])
            contexts.append(
                [chunk["text"] for chunk in retrieved_context]
            )
            ground_truths.append(item["ground_truth"])

            print("  ✓ Answer generated successfully\n")

        except Exception as exc:
            print(
                f"  ✗ Skipped due to Gemini/API error: {exc}\n"
            )
            continue

    if not questions:
        print("No evaluation samples were completed.")
        print("Gemini API is currently unavailable.")
        return

    print("===== Running RAGAS Metrics =====\n")

    dataset = Dataset.from_dict(
        {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "reference": ground_truths,
        }
    )

    result = evaluate(
        dataset,
        metrics=[
            Faithfulness(),
            AnswerRelevancy(),
            ContextPrecision(),
            ContextRecall(),
        ],
        llm=llm,
    )

    print("\n===== RAGAS Evaluation Results =====")
    print(result)


if __name__ == "__main__":
    main()