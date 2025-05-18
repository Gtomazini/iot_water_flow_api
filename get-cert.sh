#!/bin/bash

# Carregar variáveis do keys.env
source keys.env

# Criar diretórios necessários
mkdir -p certbot/conf
mkdir -p certbot/www

# Primeiro, iniciar nginx sem SSL
docker-compose up -d nginx

# Obter certificado usando as variáveis
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Reiniciar nginx com SSL
docker-compose restart nginx