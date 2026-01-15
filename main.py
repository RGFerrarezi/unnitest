import requests

def obter_nome_usuario(id_usuario):
    url = f"https://jsonplaceholder.typicode.com/todos/{id_usuario}"
    # url = "https://site-errado.com"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return "Usuário Encontrado"
        else:
            return "Usuário Inexistente"
    except requests.Timeout:
        return "Erro de Conexão"
    
def criar_usuario(nome, trabalho):
    url = "https://jsonplaceholder.typicode.com/users"
    dados = {
        "name": nome,
        "job": trabalho
    }
    try:
        resposta = requests.post(url, json=dados)
        resposta.raise_for_status()
        return resposta.json()
    except requests.Timeout:
        return "Erro de Conexão"
    except requests.HTTPError as e:
        return f"Erro HTTP: {e.response.status_code}"
    
def deletar_usuario(id_usuario):
    url = f"https://jsonplaceholder.typicode.com/users/{id_usuario}"
    try:    
        resposta = requests.delete(url)
        return resposta.status_code == 204
    except requests.Timeout:
        return False