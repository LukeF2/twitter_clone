FROM postgres:13

# Install Python and required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-psycopg2 \
    python3-venv \
    postgresql-13-rum \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install required Python packages in the virtual environment
RUN /opt/venv/bin/pip install psycopg2-binary faker werkzeug
# Copy initialization scripts
COPY schema.sql /docker-entrypoint-initdb.d/
COPY load_data.py /docker-entrypoint-initdb.d/

# Create a wait-for-db script
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

# Create an initialization script that will run after schema.sql
RUN echo '#!/bin/bash\n\
    # Wait for database to be ready\n\
    /usr/local/bin/wait-for-db.sh localhost /opt/venv/bin/python /docker-entrypoint-initdb.d/load_data.py 100' > /docker-entrypoint-initdb.d/02_load_data.sh \
    && chmod +x /docker-entrypoint-initdb.d/02_load_data.sh 