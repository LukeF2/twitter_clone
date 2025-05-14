FROM postgres:13

# Install Python and required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-psycopg2 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install required Python packages in the virtual environment
RUN /opt/venv/bin/pip install psycopg2-binary faker

# Copy initialization scripts
COPY schema.sql /docker-entrypoint-initdb.d/
COPY load_data.py /docker-entrypoint-initdb.d/

# Create an initialization script that will run after schema.sql
RUN echo '#!/bin/bash\n/opt/venv/bin/python /docker-entrypoint-initdb.d/load_data.py 100' > /docker-entrypoint-initdb.d/02_load_data.sh \
    && chmod +x /docker-entrypoint-initdb.d/02_load_data.sh 