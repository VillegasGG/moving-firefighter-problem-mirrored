# Usar la imagen base de Ubuntu 22.04
FROM ubuntu:22.04

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    git \
    python3.10 \
    python3.10-dev \
    python3-pip \
    build-essential \
    gcc \
    libpthread-stubs0-dev

# Actualizar pip
RUN python3.10 -m pip install --upgrade pip

# Establecer python3.10 como la versión predeterminada de Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Copiar el código de tu nuevo proyecto al contenedor
COPY . /usr/src/app

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Comando de entrada
CMD ["/bin/bash"]
