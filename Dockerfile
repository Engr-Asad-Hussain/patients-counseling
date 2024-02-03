FROM python:3.10-bookworm

# Set Working Directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install dos2unix

COPY project ./project
COPY patients ./patients
COPY manage.py entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
RUN dos2unix ./entrypoint.sh

# Application Environmental Variables
ENV DEBUG=False
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["./entrypoint.sh"]
