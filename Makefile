MAIN_PROGRAM	= a_maze_ing.py
VENV			= .venv
PYTHON			= python3
V_PYTHON		= $(VENV)/bin/python3
V_FLAKE			= $(VENV)/bin/flake8
V_MYPY			= $(VENV)/bin/mypy
V_PIP			= $(V_PYTHON) -m pip

DEPENDENCIES	= flake8 mypy lib/mlx-2.2-py3-none-any.whl

run:
	./$(VENV)/bin/python3 $(MAIN_PROGRAM)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

install: $(VENV)
	$(V_PIP) install $(DEPENDENCIES)

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

lint:
	$(V_FLAKE) .
	$(V_MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(V_FLAKE) .
	$(V_MYPY) . --strict

.PHONY = run clean install lint lint-strict