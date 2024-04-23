import json


def mudar_estado(arquivo: dict) -> None:

    output = arquivo["FUNCIONANDO"]
    return not output


with open("estado.json", "r+") as arquivo:
    
    arquivo_json = json.load(arquivo)
    arquivo_json["FUNCIONANDO"] = mudar_estado(arquivo_json)

    arquivo.seek(0)
    arquivo.truncate()
    arquivo.write(json.dumps(arquivo_json))

