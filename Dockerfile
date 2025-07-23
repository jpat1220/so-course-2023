# Imagen base de Python
FROM python:3
# Crear carpetas de sincronización
RUN mkdir -p /sync_files/public /sync_files/private
# Establecer el directorio de trabajo
WORKDIR /usr/src/app
# Copiar la carpeta del proyecto
COPY ./myapp/ .
# Instalar dependencias
RUN pip3 install -r requirements.txt
# Exponer el puerto 5000 (usado por Flask)
EXPOSE 5000
# Ejecutar la aplicación
CMD ["python3", "./app.py"]
