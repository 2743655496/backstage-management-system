FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

ENV DEBUG=False

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "back_stage_management_django.wsgi:application", "-b", "0.0.0.0:8000", "-w", "4"]
