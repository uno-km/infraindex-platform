---
name: testing-and-scoring
description: A skill to enforce mandatory TDD (Test-Driven Development), unit testing, scoring, and rigorous record-keeping for all new modules and features.
---

# Testing and Scoring (TDD & Record Keeping)

This skill must be activated whenever new unit features, API endpoints, or crawlers are implemented in the codebase.

## 🎯 Core Requirements

1. **Mandatory Unit Tests:** For every new function, class, API endpoint, or crawler implemented, you MUST create a corresponding unit test in the `tests/unit/` folder.
2. **Isolation & Mocking:** All tests must be completely isolated from external dependencies.
   - Use `AsyncMock` and `MagicMock` for database sessions.
   - Mock external API calls (e.g., AWS, Redis, HTTP requests).
   - Ensure tests can pass cleanly in a CI/CD environment without a live PostgreSQL or Redis instance.
3. **Run and Score (Regression):** Before concluding any feature implementation, you must execute `pytest tests/unit/ -v` and verify the results.
4. **Record Keeping:** Update the `test_report.md` artifact (or create one) documenting the exact pass/fail rates.
   - Document the test coverage (Number of Tests Passed / Total Tests).
   - Provide a "Score" (e.g., `100/100`) based on the success rate.
   - Detail any fixed errors in a "Fix Log" section for historical context.

## 📝 Workflow Example

1. **Implement Feature:** `apps/api/core/data_service.py` -> `get_latest_prices`
2. **Write Test:** `tests/unit/test_api.py` -> `test_get_latest_prices_mock_db`
3. **Execute:** Run `cmd.exe /c ".venv\Scripts\activate && pytest tests/unit/ -v"`
4. **Score & Record:** Update `test_report.md` with:
   - Module Name
   - Pass Rate
   - Fixes applied (if it failed on the first try)

> [!IMPORTANT]
> A feature is NOT considered "DONE" until it has a matching unit test that executes successfully and is logged in the test report.
