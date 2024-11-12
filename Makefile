install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Dependencies installed."

update:
	@echo "Updating dependencies..."
	pipreqs . --force
	@echo "Dependencies updated.