# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create wait-for-db script
RUN echo '#!/bin/bash\n\
    set -e\n\
    \n\
    host="$1"\n\
    shift\n\
    cmd="$@"\n\
    \n\
    until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\q"; do\n\
    >&2 echo "Postgres is unavailable - sleeping"\n\
    sleep 1\n\
    done\n\
    \n\
    >&2 echo "Postgres is up - executing command"\n\
    exec $cmd' > /usr/local/bin/wait-for-db.sh \
    && chmod +x /usr/local/bin/wait-for-db.sh

# copy project
COPY . .

# fix script permissions
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh with wait-for-db
ENTRYPOINT ["/usr/local/bin/wait-for-db.sh", "db"]
CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]
