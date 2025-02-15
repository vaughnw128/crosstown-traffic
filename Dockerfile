FROM python:3.12.2-bookworm
WORKDIR /bot

RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
        docker.io


RUN pip install poetry
COPY . .

RUN poetry install

ENTRYPOINT ["poetry"]
CMD ["poetry", "run", "uvicorn", "crosstown_traffic.main:app", "--host", "0.0.0.0", "--port", "8080"]