# Search Architecture

## 1. Overview
A multi-layered search pipeline designed to gracefully handle typos, Korean transliterations ("에이치백"), fuzzy logic, and substring matching.

## 2. Pipeline Stages
1. **Query Normalization**: Standardizes Unicode, removes excess whitespace and noise characters.
2. **Alias Resolution**: Maps inputs like "오공구공" -> "5090" -> "RTX 5090" using a verified `AliasDictionary`.
3. **Candidate Retrieval**: Fetches potential GPU models using exact match, prefix match, and trigram/fuzzy matching in PostgreSQL.
4. **Relevance Scoring**: Ranks candidates based on exactness (100%), verified alias (95%), fuzzy match (60%), and popularity.

## 3. Data Flow
- User Input -> `QueryNormalizer` -> `AliasResolver` -> `Database Query` -> `RelevanceScorer` -> `SearchResponse`.
