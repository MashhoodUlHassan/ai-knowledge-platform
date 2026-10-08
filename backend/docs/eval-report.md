# RAG Evaluation Report

## 1. Overview

The AI Knowledge Platform uses Retrieval-Augmented Generation (RAG) to retrieve relevant document chunks and generate answers using a Large Language Model (LLM).

This document describes the evaluation methodology, dataset, evaluation metrics, and current evaluation status of the RAG pipeline.

---

## 2. Evaluation Objective

The primary objectives of the evaluation are to measure:

- Answer faithfulness to retrieved context
- Answer relevance to the user's question
- Quality of retrieved context
- Coverage of relevant information
- Overall RAG pipeline reliability

---

## 3. Evaluation Dataset

The evaluation dataset contains representative questions related to:

1. Artificial Intelligence
2. Machine Learning
3. Retrieval-Augmented Generation
4. Vector Databases
5. RAG

Each evaluation sample contains:

- `question`
- `ground_truth`

The dataset is defined in:

```text
backend/evaluation/dataset.py
```

---

## 4. Evaluation Framework

The project uses **RAGAS** for automated RAG evaluation.

The evaluation script is located at:

```text
backend/evaluation/run_evaluation.py
```

The following metrics are configured:

### Faithfulness

Measures whether the generated answer is supported by the retrieved context.

Higher scores indicate that the answer is less likely to contain unsupported information.

### Answer Relevancy

Measures how relevant the generated answer is to the user's question.

Higher scores indicate that the answer directly addresses the question.

### Context Precision

Measures whether the retrieved context contains relevant information for answering the question.

Higher scores indicate better ranking and retrieval precision.

### Context Recall

Measures whether the retrieved context contains the information required to answer the question.

Higher scores indicate better retrieval coverage.

---

## 5. Evaluation Pipeline

The evaluation pipeline follows this process:

```text
Evaluation Question
        ↓
Query Validation
        ↓
Vector Retrieval
        ↓
Relevant Document Chunks
        ↓
Gemini LLM
        ↓
Generated Answer
        ↓
RAGAS Evaluation
        ↓
Evaluation Metrics
```

---

## 6. Current Evaluation Status

The RAGAS evaluation pipeline has been implemented and integrated with the existing RAG pipeline.

The evaluation script successfully loads the evaluation dataset and RAGAS metrics.

However, the complete evaluation run is currently affected by temporary Gemini API availability.

The Gemini API returned:

```text
503 UNAVAILABLE
```

with the message indicating that the selected model was experiencing high demand.

Therefore, final numerical RAGAS scores have not been recorded yet.

This is an external model availability issue rather than a failure in the evaluation pipeline implementation.

---

## 7. Evaluation Limitations

Current limitations include:

- Gemini API availability can affect evaluation runs.
- Automated evaluation requires additional LLM API calls.
- Evaluation results may vary depending on model behavior.
- A larger evaluation dataset should be used for production benchmarking.
- Human evaluation should be added alongside automated metrics.

---

## 8. Future Improvements

Future evaluation improvements include:

- Expanding the evaluation dataset
- Adding domain-specific questions
- Running evaluations periodically
- Tracking evaluation scores across versions
- Adding regression testing for RAG quality
- Adding human evaluation
- Recording evaluation results in version-controlled reports
- Comparing different embedding models
- Comparing different retrieval configurations
- Optimizing chunk size and top-k retrieval
- Monitoring hallucination and citation quality

---

## 9. Reproducibility

To run the evaluation:

```powershell
$env:PYTHONPATH="backend"
python backend\evaluation\run_evaluation.py
```

The evaluation requires the configured Gemini API credentials and the project's retrieval infrastructure to be available.

---

## 10. Conclusion

The AI Knowledge Platform currently has an automated RAG evaluation framework based on RAGAS.

The pipeline is ready to evaluate retrieval and generation quality once the Gemini API is available for the required evaluation calls.

Future evaluation runs will provide numerical scores for Faithfulness, Answer Relevancy, Context Precision, and Context Recall.