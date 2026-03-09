from rag_search import build_rag_context, search_owasp


def test_search_owasp_returns_matches_for_security_query():
    results = search_owasp("What is broken object level authorization?", top_k=2)
    assert len(results) >= 1
    assert any("authorization" in item.question.lower() for item in results)


def test_build_rag_context_handles_empty_results():
    output = build_rag_context([])
    assert output == "No relevant OWASP context found."
