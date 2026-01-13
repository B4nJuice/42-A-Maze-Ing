MAIN_PROGRAM = a_maze_ing.py

run: 
	python3 $(MAIN_PROGRAM)

clean:
	rm -rf */*__pycache__

install:
	pip install -r ./libs/requierements.txt
	pip install ./libs/mlx-2.2-py3-ubuntu-any.whl