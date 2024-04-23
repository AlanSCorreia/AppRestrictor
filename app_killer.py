# Se usar um toast com audio, assim que o audio acabar o toast não recebe mais inputs
from subprocess import run, CompletedProcess
from win11toast import toast


type Execucao = str
status_execucao = {0: 'O execução foi finalizado.',
                   128: 'O execução não foi encontrado.'}


def finalizar_execucao(execucao: Execucao) -> CompletedProcess:
    
    finalizar_pelo_gerenciador_de_tarefas = run(["taskkill", "/F", "/IM", execucao])
    return finalizar_pelo_gerenciador_de_tarefas


def notificacao_desktop(em_execucao: list) -> None:

    # tratar multiplas entradas de execução em uma só notification
    mensagem_detalhes: str

    match len(em_execucao):
        case 1: mensagem_detalhes = f"O programa {em_execucao[0].args[3]} não está autorizado a abrir agora."
        case varios_apps: mensagem_detalhes = f"Os programas {em_execucao} em questão não estão autorizados a abrir agora."

    toast("App Restrictor",
          mensagem_detalhes)


def notificar_finalizacao(apps: list):

    apenas_um_app = (len(apps) == 1)

    if apenas_um_app:
        execucao = finalizar_execucao(apps[0])
        notificacao_desktop(em_execucao=[execucao])

    else:
        execucoes = []

        for app in apps:
            execucao = finalizar_execucao(app)
            execucoes.append(execucao.returncode)
        
        notificacao_desktop(em_execucao=execucoes)
