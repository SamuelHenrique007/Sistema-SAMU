FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Converte CRLF -> LF e remove BOM; garante execução
RUN apt-get update && apt-get install -y --no-install-recommends dos2unix \
    && dos2unix entrypoint.sh \
    && sed -i '1s/^\xEF\xBB\xBF//' entrypoint.sh \
    && chmod +x entrypoint.sh \
    && apt-get purge -y dos2unix && rm -rf /var/lib/apt/lists/*


ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
CMD ["gunicorn", "samu.wsgi:application", "--bind", "0.0.0.0:8000"]

