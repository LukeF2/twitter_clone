# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# fix script permissions
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]
