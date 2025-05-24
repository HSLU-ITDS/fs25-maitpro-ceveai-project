# Backend Dockerfile
FROM python:3.13-alpine

# Install dependencies including poppler-utils
RUN apk add --no-cache \
    poppler \
    poppler-utils \
    gcc \
    musl-dev \
    build-base \
    python3-dev \
    swig \
    clang \
    clang-dev \
    llvm \
    llvm-dev

# Add poppler binaries to PATH
ENV PATH="/usr/bin:${PATH}"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]