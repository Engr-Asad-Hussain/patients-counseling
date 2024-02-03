FROM python:3.10

# Set Working Directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY project ./project
COPY patients ./patients
COPY manage.py entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

# Application Environmental Variables
ENV DEBUG=False
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["./entrypoint.sh"]