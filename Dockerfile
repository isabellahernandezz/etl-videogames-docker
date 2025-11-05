# Imagen base
FROM python:3.10-slim

# Crea un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando que se ejecuta al iniciar el contenedor
CMD ["python", "ETL.py"]
