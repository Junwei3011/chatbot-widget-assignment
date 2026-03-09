from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List

import pandas as pd
from rapidfuzz import fuzz

from config import get_settings


@dataclass
class RetrievedQA:
    question: str
    answer: str
    score: int


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    dataset_path = Path(__file__).resolve().parent / get_settings().dataset_path
    df = pd.read_csv(dataset_path)
    required_columns = {"Question", "Answer"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"dataset.csv missing columns: {', '.join(sorted(missing))}")
    return df.fillna("")


def score_row(query: str, question: str, answer: str) -> int:
    query_lower = query.lower().strip()
    question_lower = question.lower()
    answer_lower = answer.lower()

    score_question = fuzz.token_set_ratio(query_lower, question_lower)
    score_partial = fuzz.partial_ratio(query_lower, question_lower)
    score_answer = fuzz.partial_ratio(query_lower, answer_lower[:1500])

    return int(max(score_question, score_partial, score_answer * 0.85))


def search_owasp(query: str, top_k: int | None = None, min_score: int = 55) -> List[RetrievedQA]:
    df = load_dataset()
    top_k = top_k or get_settings().top_k_rag_results

    results: List[RetrievedQA] = []
    for _, row in df.iterrows():
        question = str(row["Question"]).strip()
        answer = str(row["Answer"]).strip()
        if not question or not answer:
            continue
        score = score_row(query, question, answer)
        if score >= min_score:
            results.append(RetrievedQA(question=question, answer=answer, score=score))

    results.sort(key=lambda item: item.score, reverse=True)
    return results[:top_k]


def build_rag_context(matches: List[RetrievedQA]) -> str:
    if not matches:
        return "No relevant OWASP context found."

    parts = []
    for idx, item in enumerate(matches, start=1):
        parts.append(
            f"[{idx}] OWASP Question: {item.question}\n"
            f"OWASP Answer: {item.answer}\n"
            f"Relevance Score: {item.score}"
        )
    return "\n\n".join(parts)
