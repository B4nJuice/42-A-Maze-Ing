MAIN_PROGRAM = a_maze_ing.py

run: 
	./.venv/bin/python3 $(MAIN_PROGRAM)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

install:
	pip install -r ./libs/requierements.txt
	pip install ./libs/mlx-2.2-py3-ubuntu-any.whl

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

