### A Django app to demonstrate the locking capabilities of various caching backends: database cache, LocMemCache and PyMemcacheCache. This deomnstration is inspired by https://docs.celeryq.dev/en/stable/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time
## Steps to setup
- Install Redis and make sure that it is running at port 6379 (default)
- Install memcached and make sure that it is running at port 11211 (default)
- Install the python packages in requirements in requirememts.txt
- migrate the database

##### Run the app in three different mode (using 3 different cache) using `DJANGO_SETTINGS_MODULE` environment variable. There are seperate settings files for each caching backend: `settings_db_cache.py`, `settings_local_cache.py` and `settings_pymema_cache.py` 

### Using the database cache as lock
- run `python manage.py createcachetable`
- It will create a table named my_cache_table (defined in `celery_test/settings_db_cache.py`)
- `python manage.py flush --no-input` (to clear any existing data)
- open a console and from inside of project root (celery_test/) run  `export DJANGO_SETTINGS_MODULE=celery_test.settings_db_cache`
- Now run  `./manage.py runserver`
- On your browser request `http://127.0.0.1:8000/hello`  -> This will submit the same celery task 10 times
- On another console, from inside of project root (celery_test/) run `export DJANGO_SETTINGS_MODULE=celery_test.settings_db_cache`
- `celery -A celery_test worker --loglevel=INFO`

The celery worker should start executing the tasks. Each task will race to acquire the lock. If the task acquires the lock then it will create an Invoice object in the DB (this is the objective of the task). If the locking mechanism works properly then only one task should be able to create an Invoice object . Hence, only one Invoice object should exist in the enitire DB at the end. If that is the case then we can conclude that the locking mechanism worked. I observed that only one Invoice was created.

#### Kill all the above processes

### Using  LocMemCache as lock (Mind the `export` commands, that is the only difference)
- `python manage.py flush` --no-input (to clear any existing data)
- open a console and from inside of project root (celery_test/) run  `export DJANGO_SETTINGS_MODULE=celery_test.settings_local_cache`
- Now run  `./manage.py runserver`
- On your browser request` http://127.0.0.1:8000/hello`  -> This will submit the same celery task 10 times
- On another console, from inside of project root (celery_test/) run `export DJANGO_SETTINGS_MODULE=celery_test.settings_local_cache`
- `celery -A celery_test worker --loglevel=INFO`

It was aobserved that all the 10 tasks acquired the lock and 10 inovices were created. 

#### Kill all the above processes

### Using  PyMemcacheCache as lock (Mind the `export` commands, that is the only difference)
- `python manage.py flush` --no-input (to clear any existing data)
- open a console and from inside of project root (celery_test/) run  `export DJANGO_SETTINGS_MODULE=celery_test.settings_pymema_cache`
- Now run  `./manage.py runserver`
- On your browser request http://127.0.0.1:8000/hello  -> This will submit the same celery task 10 times
- On another console, from inside of project root (celery_test/) run `export DJANGO_SETTINGS_MODULE=celery_test.settings_pymema_cache`
- `celery -A celery_test worker --loglevel=INFO`

It was aobserved that all only one task acquired the lock and only 1 inovice was created.

