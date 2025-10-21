import secrets
import string


def gerar_codigo_aleatorio(tamanho: int = 20) -> str:
    linha = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(linha) for _ in range(tamanho))