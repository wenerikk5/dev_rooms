# dev_rooms

## Description

A draft of public site for devs to discuss different topics (languages). Has been built on Django + Django Templates + Bootstrap styling. Main functionality has been covered by unittests (88% coverage).

## Set up and use

```
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# OPTIONAL: Setup database (default SQLite). Create migrations
python manage.py makemigrations
python manage.py migrate

# OPTIONAL: Fill database with test data (for all tables)
python manage.py import_users
python manage.py import_data

# Run server (default in Debug mode)
python manage.py runsever

```
Test user data:
Username: mike
Password: Abc123123


## Additional info

Created for educational purposes. 

## Preview
<img src="https://github.com/wenerikk5/dev_rooms/blob/06d2abc16d5cbdbf38f508d0ce39be0b6125d029/media/base/Preview.png" alt="img" width="800" height='600'>

