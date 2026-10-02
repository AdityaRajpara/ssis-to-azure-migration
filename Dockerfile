FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY config ./config
COPY data ./data
RUN pip install --no-cache-dir .
ENTRYPOINT ["python", "-m", "migration_demo.cli"]
CMD ["run", "--mode", "both"]
