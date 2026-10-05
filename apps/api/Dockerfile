FROM python:3.12-slim

WORKDIR /app

# Apply available Debian security updates before installing the application.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade \
    pip \
    "setuptools>=78.1.1" \
    wheel

COPY . .

ARG INSTALL_DEV=false

RUN if [ "$INSTALL_DEV" = "true" ]; then \
      python -m pip install --no-cache-dir ".[dev]"; \
    else \
      python -m pip install --no-cache-dir .; \
    fi \
    && python -m pip check

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
