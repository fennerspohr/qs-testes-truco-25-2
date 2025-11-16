import sys
import pytest
from unittest.mock import MagicMock
from truco.jogador import Jogador
sys.path.append('../qs-testes-truco-25-2')

@pytest.fixture
def jogador_mock():
    return MagicMock(spec=Jogador)

def test__init___(truco):
    """Testa a inicialização da classe Truco"""
    assert truco is not None
    assert truco.valor_aposta == 1
    assert truco.jogador_bloqueado == 0
    assert truco.jogador_pediu == 0
    assert truco.jogador_retruco == 0
    assert truco.jogador_vale_quatro == 0
    assert truco.jogador_fugiu == 0
    assert truco.estado_atual == ""

def test_inverter_jogador_bloqueado(truco):
    """Testa a inversão do jogador bloqueado"""
    truco.jogador_bloqueado = 1
    truco.inverter_jogador_bloqueado()
    assert truco.jogador_bloqueado == 2

    truco.jogador_bloqueado = 0
    truco.inverter_jogador_bloqueado()
    assert truco.jogador_bloqueado == 1

def test_inicializar_jogador_bloqueado(truco, quem_pediu=1):
    """Testa a inicialização do jogador bloqueado"""
    truco.inicializar_jogador_bloqueado(quem_pediu)
    assert truco.jogador_bloqueado == quem_pediu

def test_controlador_truco(truco, cbr_mock, dados_mock, jogador, jogador2_mock, monkeypatch):
    """ Testa situações do controlador_truco """
    # Testa quando o estado atual é "vale_quatro"
    truco.estado_atual = "vale_quatro"
    estado = truco.controlador_truco(cbr_mock, dados_mock, 1, jogador, jogador2_mock)
    assert estado is None

    # Testa quando o jogador que pediu é o bloqueado
    truco.estado_atual = ""
    truco.jogador_bloqueado = 1
    estado = truco.controlador_truco(cbr_mock, dados_mock, 1, jogador, jogador2_mock)
    assert estado is None

    # Testa quando o estado atual é ""
    truco.estado_atual = ""
    truco.jogador_bloqueado = 0
    estado = truco.controlador_truco(cbr_mock, dados_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "truco"
    assert truco.jogador_bloqueado == 1

    # Testa quando o estado atual é "truco"
    truco.estado_atual = "truco"
    truco.jogador_bloqueado = 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    estado = truco.controlador_truco(cbr_mock, dados_mock, 2, jogador, jogador2_mock)
    assert truco.estado_atual == "retruco"
    assert truco.jogador_bloqueado == 2
    assert truco.valor_aposta == 3

    # Testa quando o estado atual é "retruco"
    truco.estado_atual = "retruco"
    truco.jogador_bloqueado = 2
    monkeypatch.setattr("builtins.input", lambda _: "2")
    estado = truco.controlador_truco(cbr_mock, dados_mock, 3, jogador, jogador2_mock)
    assert truco.estado_atual == "vale_quatro"
    assert truco.jogador_bloqueado == 1
    assert truco.valor_aposta == 4

def test_pedir_truco(truco, cbr_mock, jogador, jogador2_mock, monkeypatch):
    """Testa o método pedir_truco"""
    #Caso 1: jog1 ped truco, jog2 aceita
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 1
    estado = truco.pedir_truco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "truco"
    assert truco.jogador_bloqueado == 1
    assert estado is True

    # Caso 2: jog1 ped truco, jog2 recusa
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 0
    estado = truco.pedir_truco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "truco"
    assert truco.jogador_bloqueado == 1
    assert estado is False
    assert jogador.pontos == 1

    # Caso 2: jog1 ped truco, jog2 aumenta
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 2
    monkeypatch.setattr("builtins.input", lambda _: '0')
    estado = truco.pedir_truco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.jogador_bloqueado == 2

    # Caso 4: jog2 ped truco, jog1 recusa
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    monkeypatch.setattr("builtins.input", lambda _: '0')
    estado = truco.pedir_truco(cbr_mock, 2, jogador, jogador2_mock)
    assert truco.estado_atual == "truco"
    assert truco.jogador_bloqueado == 2
    assert estado is False
    assert jogador2_mock.pontos == 1

def test_pedir_retruco(truco, cbr_mock, jogador, jogador2_mock, monkeypatch):
    """Testa o método pedir_retruco"""
    #Caso 1: jog1 pede retruco, jog2 aceita
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 1
    estado = truco.pedir_retruco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "retruco"
    assert truco.jogador_bloqueado == 1
    assert estado is True

    # Caso 2: jog1 pede retruco, jog2 recusa
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 0
    estado = truco.pedir_retruco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "retruco"
    assert truco.jogador_bloqueado == 1
    assert estado is False
    assert jogador.pontos == 2

    # Caso 2: jog1 pedee retruco, jog2 aumenta
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    jogador2_mock.avaliar_truco.return_value = 2
    monkeypatch.setattr("builtins.input", lambda _: '0')
    estado = truco.pedir_retruco(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.jogador_bloqueado == 2

    # Caso 4: jog2 pede retruco, jog1 recusa
    jogador.pontos = 0
    jogador2_mock.pontos = 0
    monkeypatch.setattr("builtins.input", lambda _: '0')
    estado = truco.pedir_retruco(cbr_mock, 2, jogador, jogador2_mock)
    assert truco.estado_atual == "retruco"
    assert truco.jogador_bloqueado == 2
    assert estado is False
    assert jogador2_mock.pontos == 2

def test_pedir_vale_quatro(truco, cbr_mock, jogador, jogador2_mock, monkeypatch):
    """Testa o método pedir_vale_quatro"""
    #Caso 1: jog1 pede vale quatro, jog2 aceita
    jogador2_mock.avaliar_truco.return_value = 1
    estado = truco.pedir_vale_quatro(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "vale_quatro"
    assert truco.jogador_bloqueado == 1
    assert estado is True

    # Caso 2: jog1 pede vale quatro, jog2 recusa
    jogador2_mock.avaliar_truco.return_value = 0
    estado = truco.pedir_vale_quatro(cbr_mock, 1, jogador, jogador2_mock)
    assert truco.estado_atual == "vale_quatro"
    assert truco.jogador_bloqueado == 1
    assert estado is False
    assert jogador.pontos == 3

    # Caso 4: jog2 pede vale quatro, jog1 recusa
    monkeypatch.setattr("builtins.input", lambda _: '0')
    estado = truco.pedir_vale_quatro(cbr_mock, 2, jogador2_mock, jogador)
    assert truco.estado_atual == "vale_quatro"
    assert truco.jogador_bloqueado == 2
    assert estado is False
    assert jogador2_mock.pontos == 3

def test_retornar_valor_aposta(truco):
    """Testa o método retornar_valor_aposta"""
    assert truco.retornar_valor_aposta() == 1
    truco.valor_aposta = 3
    assert truco.retornar_valor_aposta() == 3
    truco.valor_aposta = 4
    assert truco.retornar_valor_aposta() == 4

def test_retornar_quem_fugiu(truco):
    """Testa o método retornar_quem_fugiu"""
    truco.jogador_fugiu = 1
    assert truco.retornar_quem_fugiu() == 1
    truco.jogador_fugiu = 2
    assert truco.retornar_quem_fugiu() == 2
    truco.jogador_fugiu = 0
    assert truco.retornar_quem_fugiu() == 0

def test_resetar(truco):
    """Testa o reset dos atributos da classe Truco"""
    truco.valor_aposta = 3
    truco.jogador_bloqueado = 2
    truco.jogador_pediu = 1
    truco.jogador_retruco = 1
    truco.jogador_vale_quatro = 2
    truco.jogador_fugiu = 1
    truco.estado_atual = "truco"

    truco.resetar()

    assert truco.valor_aposta == 1
    assert truco.jogador_bloqueado == 0
    assert truco.jogador_pediu == 0
    assert truco.jogador_retruco == 0
    assert truco.jogador_vale_quatro == 0
    assert truco.jogador_fugiu == 0
    assert truco.estado_atual == ""

