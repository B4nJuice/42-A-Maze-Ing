MAIN_PROGRAM	= a_maze_ing.py
VENV			= .venv
PYTHON			= python3
V_PYTHON		= $(VENV)/bin/python3
V_FLAKE			= $(VENV)/bin/flake8
V_MYPY			= $(VENV)/bin/mypy
V_PIP			= $(V_PYTHON) -m pip

SRCS			= a_maze_ing.py ./src

DEPENDENCIES	= flake8 mypy lib/mlx-2.2-py3-none-any.whl

run: install
	./$(VENV)/bin/python3 $(MAIN_PROGRAM)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

install: $(VENV)
	$(V_PIP) install $(DEPENDENCIES)

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

lint: install
	$(V_FLAKE) $(SRCS)
	$(V_MYPY) $(SRCS) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(V_FLAKE) $(SRCS)
	$(V_MYPY) $(SRCS) --strict


.PHONY = run clean fclean install lint lint-strict