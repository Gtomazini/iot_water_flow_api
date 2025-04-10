from pytest_bdd import scenario, given, when, then, parsers

CONTEXT = {}
@scenario('../leitura_agua.feature', 'Receber leitura instantanea')
def test_publish():
    pass

@given(parsers.parse('uma torneira com um sensor "{id_sensor}" conectado'))
def check_link(id_sensor):
    if id_sensor == "AG01":
        return True
    else:
        return "Sensor não encontrado"

@when("chega uma leitura o sistema checa a chave de autenticacao")
def auth_sensor(id_sensor, leitura_externa):
    id_sensor = CONTEXT['id_sensor']
    CONTEXT['autenticado'] = (id_sensor == "AG01")
    return CONTEXT['autenticado']


@then("o sistema recebe essa leitura com sucesso caso autenticado")
def instantaneous_reader(leitura: str):
    assert CONTEXT['autenticado, leitura isntantanea'], "Sensor não autenticado"

@given("um sistema que aguarda uma requisicao de um sensor")
def await_request():
    pass

@when(parsers.parse('recebe a requisicao do sensor "{novo_id_sensor}" contendo "{timestamp_inicial}" de tempo '
                    'inicial com "{timestamp_final}" de tempo final e um fluxo médio de "{fluxo_medio}"'))
def receiver_data(novo_id_sensor, timestamp_inicial, timestamp_final, fluxo_medio):
    CONTEXT['novo_id_sensor'] = novo_id_sensor
    CONTEXT['timestamp_inicial'] = timestamp_inicial
    CONTEXT['timestamp_final'] = timestamp_final
    CONTEXT['fluxo_medio'] = fluxo_medio
    pass

@then('o sistema calcula um volume total de "{result}" metros cubicos')
def calculus_volume(result):
    pass



