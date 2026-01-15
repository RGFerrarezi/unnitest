# test_api.py

# pip install pytest requests
# pip install pytest-cov

# testar vendo quais linhas do api foram usadas
# pytest --cov=main -v

# testar apenas o arquivo de teste
# pytest -v


import requests
import pytest
from main import obter_nome_usuario, criar_usuario, deletar_usuario
from unittest.mock import Mock, patch

def test_api_esta_online():    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
             
        resposta = obter_nome_usuario(1)
        mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/todos/1")
        assert resposta == "Usuário Encontrado"
    
@pytest.mark.parametrize("id_usuario", [999,888,777,2,3,0])
def test_api_nao_encontrada(id_usuario):
    with patch('requests.get') as mock_get:    
        mock_get.return_value.status_code = 404
        resposta = obter_nome_usuario(id_usuario)
        mock_get.assert_called_once_with(f"https://jsonplaceholder.typicode.com/todos/{id_usuario}")
        assert resposta == "Usuário Inexistente"
    
    
def test_api_timeout():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.Timeout()
        resposta = obter_nome_usuario("timeout")
        mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/todos/timeout")
        assert resposta == "Erro de Conexão"
    
def test_criar_usuario_sucesso():
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"id": 151}
        resposta = criar_usuario("Kastarys", "Developer")
        mock_post.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            json={"name": "Kastarys", "job": "Developer"}
        )
        assert resposta["id"] == 151
    
def test_criar_usuario_dados_invalidos():
    with patch('requests.post') as mock_post:
        erro_fake = requests.HTTPError("Erro Simulado")
        
        erro_fake.response = Mock(status_code=400)
        
        mock_post.return_value.raise_for_status.side_effect = erro_fake
        
        resposta = criar_usuario("", "")
        
        mock_post.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            json={"name": "", "job": ""}
        )
        assert resposta == "Erro HTTP: 400"
    
def test_criar_usuario_timeout():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.Timeout
        
        resposta = criar_usuario("Timeout", "Anything")
        assert resposta == "Erro de Conexão"
        
        
def test_delete_usuario():
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.status_code = 204
        
        resposta = deletar_usuario(1)
        
        mock_delete.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")
        assert resposta == True
        
def test_delete_usuario_timeout():
    with patch('requests.delete') as mock_delete:
        mock_delete.side_effect = requests.Timeout
        
        resposta = deletar_usuario(999)
        
        mock_delete.assert_called_once_with("https://jsonplaceholder.typicode.com/users/999")
        assert resposta == False
        
# Descomente para rodar teste de integração real com a API externa
# @pytest.mark.integracao
# def test_real_obter_usuario_1():
#     print("\n--- Acessando API Real... ---")
#     resposta = obter_nome_usuario(1)
    
#     assert resposta == "Usuário Encontrado"