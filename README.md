# Stock Market Django app

This purpose of this rudimentary Django CMS website is to provide web visitors the ability to build their own stock market / mutual fund / commodity / crypto currency watch list.


### BUILD INSTRUCTIONS

For *nix:
```
$ virtualenv --python=python3.8 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py makemigrations
$ python manage.py runserver
```

Based on John Elder's Udemy course on how to build a stock market quote web app. [More details here](https://www.udemy.com/course/build-a-stock-market-web-app-with-python-and-django/learn/lecture/15727744#overview).