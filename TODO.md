# Test Fix Plan

## Problem

Multiple concurrent pytest processes running against the same `SCHOOL_ERP_TEST` database. The session-scoped `setup_database` fixture calls `Base.metadata.drop_all()` at session end, which drops tables that other concurrent test sessions still need, causing `relation "users" does not exist` / `relation "week_days" does not exist` errors.

## Solution

Modify the `db_session` fixture in `tests/conftest.py` to call `Base.metadata.create_all()` at the start of each test. This ensures tables exist even if another test process dropped them.

## Steps

- [x] Step 1: Analyze root cause
- [x] Step 2: Fix `tests/conftest.py` - Add `create_all` to `db_session` fixture
- [x] Step 3: Verify by running tests - ✅ 215 passed, 14 xfailed (0 errors)
- [x] Step 4: Run the project

## Results Summary

- **Total tests**: 229 (215 passed + 14 expected failures)
- **Errors**: 0
- **Failures**: 0
- **14 xfailed tests**: These are pre-existing known issues in timetable tests (e.g., schema type mismatches for `class_subject_id`/`teacher_subject_id` as int vs string, `ClassSubject.subject_name` attribute missing) that were already documented in the test code before our changes.
