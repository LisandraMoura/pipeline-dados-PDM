# Imagem base do Python
FROM python:3.8-slim

# Diretório de trabalho no container
WORKDIR /app

# Copiar arquivos para o container
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta para o Flask
EXPOSE 8080

# Comando para rodar o app
CMD ["python", "app.py"]
