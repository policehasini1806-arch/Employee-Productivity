# Employee Productivity Digital Twin (Django)

1. Put `employee_productivity_model.pkl` (your notebook's model) next to `manage.py`.
   No .pkl? Run `python train_model.py` to create one.
2. python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
3. python manage.py migrate
   python manage.py runserver
4. Open http://127.0.0.1:8000/  (dashboard)  and /predict/ (form)
