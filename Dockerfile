FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (libgomp1 is required by scikit-learn / OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create uvicorn wrapper that sanitizes literal '$PORT' argument passed by cloud runners
RUN printf '#!/bin/sh\n\
ARGS=""\n\
PORT_VAL="${PORT:-8000}"\n\
while [ "$#" -gt 0 ]; do\n\
  case "$1" in\n\
    --port)\n\
      shift\n\
      if echo "$1" | grep -Eq "^[0-9]+$"; then\n\
        ARGS="$ARGS --port $1"\n\
      else\n\
        ARGS="$ARGS --port $PORT_VAL"\n\
      fi\n\
      shift\n\
      ;;\n\
    *)\n\
      ARGS="$ARGS \"$1\""\n\
      shift\n\
      ;;\n\
  esac\n\
done\n\
eval exec python -m uvicorn $ARGS\n' > /usr/local/bin/uvicorn && chmod +x /usr/local/bin/uvicorn

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["python", "backend/app.py"]
