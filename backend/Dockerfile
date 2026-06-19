FROM python:3.13.5

ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUBUFFERED=1

WORKDIR /backapp

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:10000"]