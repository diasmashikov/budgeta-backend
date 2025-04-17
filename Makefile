run:
	flask run

init-db:
	flask init-db

load-libs:
	pip install -r requirements.txt


delete-db:
	rm instance/budget_tracker.db

