install:  # сборка проекта
	uv sync

dev: 
	uv run flask --debug --app page_analyzer:app run

test:
	uv run ruff check .