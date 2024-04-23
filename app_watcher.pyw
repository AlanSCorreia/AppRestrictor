import json
import app_killer
from time import sleep, localtime
from subprocess import run


def intervalo_valido(comeco_intervalo: int, fim_intervalo: int):

    horas = localtime()[3]
    return horas in range(comeco_intervalo, fim_intervalo)


def checando_estado():

    with open("estado.json", "r") as arquivo:
        estado = json.load(arquivo)
    
    return estado["FUNCIONANDO"]


def app_esta_rodando() -> list:

    processos_executando: list[str] = run(['tasklist'], capture_output=True, text=True)
    return [app for app in apps_restringidos if app in processos_executando.stdout]


with open("apps_restringidos.json", "r") as arquivo:
    apps = json.load(arquivo)
    apps_restringidos: list[str] = [app for app in apps["apps"]]
    comeco_intervalo, fim_intervalo = apps["horarios"]


while checando_estado():

    apps_ilegais_rodando = app_esta_rodando()
    app_esta_rodando_em_intervalo_invalido = (any(apps_ilegais_rodando) and \
                                             not intervalo_valido(comeco_intervalo=comeco_intervalo,
                                                                  fim_intervalo=fim_intervalo))

    if app_esta_rodando_em_intervalo_invalido:
        app_killer.notificar_finalizacao(apps_ilegais_rodando)
    
    sleep(10)
