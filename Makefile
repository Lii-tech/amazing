run:
	python -m mazegen.a_maze_ing mazegen/config.txt

debug:
	python -m pdb -m mazegen.a_maze_ing

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build
	rm -f maze.txt
	
lint:
	python3 -m flake8 .
	python3 -m mypy \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \

lint-strict:
	python3 -m flake8 .
	python3 -m mypy --strict .
