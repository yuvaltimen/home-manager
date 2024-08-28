FROM python:3.11.1-slim-buster AS builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /home_manager

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip  && pip install --no-cache-dir -Ur /home_manager/requirements.txt

COPY . .
RUN chmod +x /home_manager/entrypoint.sh

RUN python -m pytest /home_manager/tests/*


FROM python:3.11.1-slim-buster AS runner

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends netcat

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /home_manager/manage.py /home_manager/manage.py
COPY --from=builder /home_manager/entrypoint.sh /home_manager/entrypoint.sh
COPY --from=builder /home_manager/app /home_manager/app
COPY --from=builder /home_manager/home_manager /home_manager/home_manager
COPY --from=builder /home_manager/users /home_manager/users
COPY --from=builder /home_manager/media /home_manager/media

ENV PATH="/opt/venv/bin:$PATH"

RUN chmod +x /home_manager/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/home_manager/entrypoint.sh"]
