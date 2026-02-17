MAIN_PROGRAM	= a_maze_ing.py
VENV			= .venv
PYTHON			= python3
V_PYTHON		= $(VENV)/bin/python3
V_FLAKE			= $(VENV)/bin/flake8
V_MYPY			= $(VENV)/bin/mypy
V_PIP			= $(V_PYTHON) -m pip

OUTPUT_FILE		= mazegen-1.0.0-py3-none-any.whl

SRCS			= $(MAIN_PROGRAM) ./src

DEPENDENCIES	= flake8 mypy lib/mlx-2.2-py3-none-any.whl build

run:
	$(V_PYTHON) $(MAIN_PROGRAM)

build: $(OUTPUT_FILE)

$(OUTPUT_FILE): $(SRCS)
	$(V_PYTHON) -m build -o .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

install: $(VENV)
	$(V_PIP) install $(DEPENDENCIES)
	$(MAKE) build
	$(V_PIP) install $(OUTPUT_FILE) --force-reinstall

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

lint: install
	$(V_FLAKE) $(SRCS)
	$(V_MYPY) $(SRCS) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(V_FLAKE) $(SRCS)
	$(V_MYPY) $(SRCS) --strict

debug: install
	$(PYTHON) -m pdb $(MAIN_PROGRAM)

.PHONY: run clean fclean install lint lint-strict build