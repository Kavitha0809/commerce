# commerce
CS50 PROJECT

## Prerequisites

- Python 3.x
- pip package manager

## Setup Instructions

1. *Create a virtual environment:*

   bash
   python -m venv env
2. **Activate the virtual environment:**
   bash
   source env/bin/activate
3. *Install the project dependencies:*
	 bash
	pip install -r requirements.txt
4. **Apply database migrations:**
	 bash
	 python manage.py makemigrations
	python manage.py migrate
5. *Start the development server:*
	```bash
	python manage.py runserver
6. *Start the development server:*
	Open a web browser and visit [http://localhost:8000](http://localhost:8000/) to view the application.

