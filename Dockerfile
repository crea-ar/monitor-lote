FROM python:3.12-alpine AS builder

WORKDIR /app

RUN apk update && apk add --no-cache \
    build-base \
    gdal \
    gdal-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    bash \
    curl

COPY requirements.txt .

# Instalamos dependencias en un directorio separado
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.12-alpine

WORKDIR /app

# Instalar solo lo necesario para ejecutar la app
RUN apk add --no-cache \
    gdal \
    bash \
    curl

COPY --from=builder /install /usr/local
COPY run_app.sh .
COPY requirements.txt .

RUN chmod +x run_app.sh

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["/bin/sh"]
CMD ["./run_app.sh"]
