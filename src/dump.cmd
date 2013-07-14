@echo off
python manage.py dumpdata -n --indent=4 --format=json users communities | python fix_json.py
python manage.py dumpdata -n --indent=4 --format=json meetings.meeting | python fix_json.py
python manage.py dumpdata -n --indent=4 --format=json issues | python fix_json.py
python manage.py dumpdata -n --indent=4 --format=json meetings --exclude meetings.meeting | python fix_json.py
