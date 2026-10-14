# CampusFlow AI Learning Log

## Engineer A
**Responsibilities:** Ticket creation, input validation, priority engine, persistence storage 
and automated tests.

### Log 1: Ticket Creation
**Problem:** Generate unique ticket IDs (T001, T002, etc.).

**AI Assistance:** AI explained how to use loops, string slicing, and f-strings to generate sequential IDs.

**What I Learned:** How `f"T{highest_id + 1:03d}"` generates ticket IDs.

**Verification:** Tested ticket creation and unique IDs using unittest. Tests passed.

### Log 2: Input Validation and Priority Engine
**Problem:** Validate ticket information and calculate priority correctly.

**AI Assistance:** AI explained conditional statements, ValueError, and priority rules.

**What I Learned:** How to reject invalid inputs and calculate critical, high, medium, and low priorities.

**Verification:** Tested valid and invalid inputs and all four priority levels. Tests passed.

### Log 3: Automated Testing
**Problem:** Verify that ticket creation, validation, and priority calculation work correctly.

**AI Assistance:** AI explained unittest, assertEqual(), assertRaises(), and setUp().

**What I Learned:** How to write automated tests and check expected results.

**Verification:** Ran `python3 -m unittest discover -s tests -v`. All 16 Engineer A ticket tests passed.

### Summary
AI helped me understand Python concepts, improve my implementation, and write automated tests. I verified my work through testing.

# CampusFlow AI Learning Log

## Engineer B

**Responsibilities:** Ticket assignment, status management, work queue, reports, and automated testing.

### Log 1: Ticket Assignment and Status Management

**Problem:** Assign tickets correctly and ensure they follow valid status transitions.

**AI Assistance:** AI explained ticket lookup, input validation, conditional statements, and `ValueError`.

**What I Learned:** How to assign staff members and manage ticket statuses safely.

**Verification:** Created tests for valid assignments, invalid inputs, and status transitions.

### Log 2: Work Queue and Reports

**Problem:** Organize unresolved tickets by priority and generate ticket statistics.

**AI Assistance:** AI explained sorting, lambda functions, dictionaries, and loops.

**What I Learned:** How to sort tickets and count tickets by status and priority.

**Verification:** Created tests for queue ordering, resolved tickets, and report accuracy.

### Log 3: Automated Testing

**Problem:** Verify that Engineer B's functions work correctly.

**AI Assistance:** AI explained Python's `unittest`, `setUp()`, `assertEqual()`, and `assertRaises()`.

**What I Learned:** How to test expected results and handle invalid situations.

**Verification:** Prepared 23 automated tests to check Engineer B's functions.

### Summary

AI helped me understand ticket management, queue sorting, report generation, and automated testing. I prepared tests to verify my work and improve CampusFlow's reliability.
