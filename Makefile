compile:
	mkdir -p scripts
	jupyter nbconvert --to script main_sender.ipynb --output-dir scripts
	jupyter nbconvert --to script main_worker.ipynb --output-dir scripts