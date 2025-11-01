#!/bin/bash

echo "🔐 Script de Geração de Certificado SSL - WaterGame API"
echo "========================================================"
echo ""

# Carregar variáveis do keys.env
if [ ! -f keys.env ]; then
    echo "❌ Erro: Arquivo keys.env não encontrado!"
    exit 1
fi

source keys.env

echo "📋 Configurações:"
echo "   Domain: $DOMAIN"
echo "   Email: $EMAIL"
echo ""

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p certbot/conf
mkdir -p certbot/www
mkdir -p certbot/www/.well-known/acme-challenge

# Fazer backup do nginx.conf atual
if [ -f nginx.conf ]; then
    echo "💾 Fazendo backup do nginx.conf..."
    cp nginx.conf nginx.conf.backup
fi

# Usar configuração temporária do nginx (sem SSL)
echo "⚙️  Usando nginx temporário (sem SSL)..."
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    sendfile on;
    keepalive_timeout 65;

    upstream fastapi {
        server watergame-api:8000;
    }

    server {
        listen 80;
        listen [::]:80;
        server_name DOMAIN_PLACEHOLDER;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
            try_files $uri =404;
        }

        location / {
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Substitui o placeholder pelo domínio real
sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" nginx.conf

# Para todos os containers
echo "🛑 Parando containers..."
docker-compose down

# Sobe apenas nginx e api
echo "🚀 Iniciando nginx e API..."
docker-compose up -d watergame-api nginx

# Aguarda alguns segundos
echo "⏳ Aguardando nginx inicializar..."
sleep 5

# Testa o acme-challenge
echo "🧪 Testando acesso ao acme-challenge..."
mkdir -p certbot/www/.well-known/acme-challenge/
echo "test123" > certbot/www/.well-known/acme-challenge/test
sleep 2

CHALLENGE_TEST=$(curl -s http://localhost/.well-known/acme-challenge/test)
if [ "$CHALLENGE_TEST" == "test123" ]; then
    echo "✅ Teste local OK!"
else
    echo "⚠️  Teste local retornou: $CHALLENGE_TEST"
    echo "⚠️  Continuando mesmo assim..."
fi

# Testa externamente
echo "🌐 Testando acesso externo..."
EXTERNAL_TEST=$(curl -s http://$DOMAIN/.well-known/acme-challenge/test)
if [ "$EXTERNAL_TEST" == "test123" ]; then
    echo "✅ Teste externo OK!"
else
    echo "⚠️  Teste externo retornou: $EXTERNAL_TEST"
    echo "⚠️  Pode haver problemas com DNS ou firewall..."
fi

rm certbot/www/.well-known/acme-challenge/test

# Obter certificado
echo ""
echo "🔐 Solicitando certificado SSL..."
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --non-interactive \
    -d $DOMAIN

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Certificado gerado com sucesso!"
    echo ""
    
    # Agora usa o nginx.conf completo com SSL
    echo "⚙️  Configurando nginx com SSL..."
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    sendfile on;
    keepalive_timeout 65;

    upstream fastapi {
        server watergame-api:8000;
    }

    server {
        listen 80;
        listen [::]:80;
        server_name DOMAIN_PLACEHOLDER;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
            try_files $uri =404;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name DOMAIN_PLACEHOLDER;

        ssl_certificate /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        location / {
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
            try_files $uri =404;
        }
    }
}
EOF
    
    # Substitui o placeholder pelo domínio real
    sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" nginx.conf
    
    # Reinicia com SSL
    echo "🔄 Reiniciando containers com SSL..."
    docker-compose down
    docker-compose up -d
    
    echo ""
    echo "🎉 Tudo pronto!"
    echo ""
    echo "✅ Teste seu site: https://$DOMAIN"
    echo ""
    echo "📝 Próximos passos:"
    echo "   1. Configure renovação automática adicionando ao crontab:"
    echo "      0 3 * * * cd $(pwd) && docker-compose run --rm certbot renew --quiet && docker-compose restart nginx"
    echo ""
else
    echo ""
    echo "❌ Erro ao gerar certificado!"
    echo ""
    echo "Possíveis causas:"
    echo "   1. DNS não aponta para este servidor"
    echo "   2. Firewall bloqueando porta 80"
    echo "   3. Cloudflare com proxy ativado (veja solução abaixo)"
    echo ""
    echo "💡 Solução para Cloudflare:"
    echo "   No painel do Cloudflare, desative temporariamente o proxy (nuvem laranja)"
    echo "   para o registro DNS do seu domínio, gere o certificado, e depois reative."
    echo ""
    
    # Restaura backup se existir
    if [ -f nginx.conf.backup ]; then
        echo "↩️  Restaurando nginx.conf anterior..."
        mv nginx.conf.backup nginx.conf
        docker-compose restart nginx
    fi
    
    exit 1
fi
