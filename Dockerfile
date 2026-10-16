FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt* pyproject.toml* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir . 2>/dev/null || true
COPY . .
LABEL org.opencontainers.image.source="https://github.com/mafzalkalwardev/clientreadyftsolutionsdombom"
CMD ["python", "-c", "print('clientreadyftsolutionsdombom image ready')"]
