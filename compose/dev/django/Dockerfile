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

COPY ./compose/dev/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/dev/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/dev/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/dev/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN python -m pytest /home_manager/tests/*


FROM python:3.11.1-slim-buster AS runner

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends netcat

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /home_manager/ /home_manager/

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

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["/entrypoint"]
