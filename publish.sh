#!/bin/sh
HOST=ubuntu@cloud.crechefarandole.com
REMOTE=/home/ubuntu/inventaire/

# transfer files
rsync -azv --include-from=include.txt --exclude '*' --delete . $HOST:$REMOTE

# collect static / change to DEBUG = False / reload apache
ssh $HOST "cd ${REMOTE} ; source venv/bin/activate; python manage.py collectstatic --no-input -c -l ; sed -i '/DEBUG = True/c\DEBUG = False' website/settings.py ; touch website/wsgi.py"
