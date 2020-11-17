ARG IMG_VERSION=3.7

FROM python:$IMG_VERSION

COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

# atualiza o pip e instala o pade e outras dependencias se existirem

RUN python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt

# copia todo o contexto para dentro do container a fim de otimizar o tempo de build

COPY . /opt/app

EXPOSE 8000

