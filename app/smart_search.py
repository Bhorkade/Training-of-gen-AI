from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def smart_search(records, question):
    if not records or not question.strip():
        return []

    documents = []

    for record in records:
        text = " ".join([
            str(record.get("title", "")),
            str(record.get("category", "")),
            str(record.get("description", "")),
            str(record.get("eligibility", "")),
            str(record.get("source", ""))
        ])
        documents.append(text)

    try:
        vectorizer = TfidfVectorizer(stop_words="english")

        record_vectors = vectorizer.fit_transform(documents)
        question_vector = vectorizer.transform([question])

        scores = cosine_similarity(
            question_vector,
            record_vectors
        ).flatten()

        ranked_indices = scores.argsort()[::-1][:3]

        results = []

        for index in ranked_indices:
            if scores[index] > 0:
                result = records[index].copy()
                result["similarity_score"] = round(
                    float(scores[index]), 3
                )
                results.append(result)

        return results

    except ValueError:
        return []