rm -rf venv;

rm -rf .mypy_cache;

find . -type f -name "*.py[co]" -delete;
find . -type d -name "__pycache__" -delete;

rm -rf .pytest_cache

rm -f .coverage
rm -f coverage.xml
rm -f coverage.json
rm -rf htmlcov
