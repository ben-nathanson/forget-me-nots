rm -rf venv;
rm -rf .mypy_cache;
find . -type f -name "*.py[co]" -delete;
find . -type d -name "__pycache__" -delete;
