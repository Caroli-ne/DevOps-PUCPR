# Use Python 3.11 slim como base para menor tamanho
FROM python:3.11-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Cria usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY src/ ./src/

# Muda proprietário dos arquivos para o usuário não-root
RUN chown -R appuser:appuser /app

# Muda para usuário não-root
USER appuser

# Expõe a porta da aplicação
EXPOSE 8000

# Healthcheck para verificar se a aplicação está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Comando para executar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
