FROM python:3.11.1-slim-buster AS builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /home_manager

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./home_manager .
RUN pip install --upgrade pip  && pip install --no-cache-dir -Ur /home_manager/requirements.txt

COPY ./compose/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/prod/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/prod/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/prod/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/prod/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN python -m pytest /home_manager/tests/*



FROM python:3.11.1-slim-buster AS runner

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /home/django_app

RUN addgroup --system django_app && adduser --system --group django_app

ENV HOME=/home/django_app
ENV APP_HOME=/home/django_app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends netcat

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /home_manager/ ./

COPY --from=builder /entrypoint /entrypoint
COPY --from=builder /start /start
COPY --from=builder /start-celeryworker /start-celeryworker
COPY --from=builder /start-celerybeat /start-celerybeat
COPY --from=builder /start-flower /start-flower

RUN chmod +x /entrypoint
RUN chmod +x /start
RUN chmod +x /start-celeryworker
RUN chmod +x /start-celerybeat
RUN chmod +x /start-flower

RUN chown -R django_app:django_app $APP_HOME
RUN chown -R django_app:django_app /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

USER django_app

ENTRYPOINT ["/entrypoint"]
