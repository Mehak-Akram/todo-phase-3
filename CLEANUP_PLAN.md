# Project Cleanup Plan

## SAFE TO DELETE

### Python Cache Files
- All `__pycache__` directories
- All `.pyc` files

### Temporary Files
- `tmpclaude-*` files throughout the project
- `backend/todo_app.db` (replaced by `todo_app_local.db`)
- Various temporary cache files

### Potentially Redundant Test Files
- `test_basic.py` (likely redundant with other tests)
- `test_api_connection.py` (may be redundant)

## REVIEW BEFORE DELETE

### Similar Test Files
- Compare `final_comprehensive_test.py` vs `test_comprehensive.py` vs `test_enhanced.py`
- Compare `test_todo_creation.py` vs `test_todo_persistence.py` vs `test_position_based_deletion.py`
- Compare `test_original_issue.py` vs `test_specific_issues.py`

### Potentially Unused Files
- `todo_app.py` in root (LEGACY - confirmed as phase 1 implementation, safe to delete)
- Some debug files like `debug_chat_api.py`, `debug_database.py`, `debug_todo_creation.py` (development files, safe to delete)
- Root-level test files that duplicate backend/tests/ files (safe to delete)
- Various temporary verification files

## DO NOT TOUCH

### Critical Core Files
- All main application files in `backend/src/`
- All frontend components and pages
- Main API routes and services
- Essential configuration files
- Active database files (`todo_app_local.db`)
- Chatbot implementation files
- Authentication system