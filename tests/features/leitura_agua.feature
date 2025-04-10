Feature: Recebimento de leitura
  Um dispositivo de leitura de consumo de água
  Ele envia dados para o sistema
  O sistema armazena e processa esses dados

  Scenario: Receber leitura instantanea
    Dado uma torneira com um sensor "AG01" conectado
    Quando chega uma leitura o sistema checa a chave de autenticacao
    Então o sistema recebe essa leitura com sucesso caso autenticado



  Scenario: Receber leitura baseado no consumo
    Dado um sistema que aguarda uma requisicao de um sensor
    Quando recebe a requisicao do sensor "AG01" contendo "2025-04-10T14:30:00" de tempo inicial com
  "2025-04-10T14:31:30" de tempo final e um fluxo médio de "0.0025":
    Então o sistema calcula um volume total de 0.00375 metros cubicos