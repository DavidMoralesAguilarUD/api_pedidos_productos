# Usa una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app


COPY requirements.txt .

# Instalar las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copiar los archivos del proyecto al contenedor


COPY . .

# Instalar Flask
RUN pip install Flask

# Exponer el puerto en el que correrá la app Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
