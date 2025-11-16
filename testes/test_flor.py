import sys
import pytest
sys.path.append('../qs-testes-truco-25-2')
from truco.flor import Flor
from testes import conftest

def test___init___(flor):
    assert flor is not None
    assert flor.valor_flor == 3
    assert flor.quem_pediu_flor == 0
    assert flor.quem_pediu_contraflor == 0
    assert flor.quem_pediu_contraflor_resto == 0
    assert flor.quem_venceu_flor == 0
    assert flor.estado_atual == ""

def test_pedir_flor(flor, jogador, jogador2, interface_mock, monkeypatch):
    """"Testa primeiro if"""
    flor.pedir_flor(2, jogador, jogador2, interface_mock)
    assert jogador.pediu_flor == False
    assert jogador2.pediu_flor == True
    assert flor.estado_atual == "Flor"

    """Testa contraflor e resto"""
    flor.estado_atual = ""
    jogador.flor = True
    jogador2.flor = True
    jogador.pontos = 5
    jogador2.pontos = 2
    monkeypatch.setattr(flor, "decisao_jogador", lambda: True)
    flor.pedir_flor(1, jogador, jogador2, interface_mock)
    assert flor.estado_atual == "Contraflor e Resto"
    assert flor.quem_venceu_flor == 1
    
    """Testa else contraflor e resto"""
    flor.estado_atual = ""
    jogador.flor = True
    jogador2.flor = True
    jogador.pontos = 5
    jogador2.pontos = 2
    monkeypatch.setattr(flor, "decisao_jogador", lambda: False)
    flor.pedir_flor(1, jogador, jogador2, interface_mock) 
    assert flor.estado_atual == "Contraflor e Resto"
    assert jogador2.pontos == 6 

    """Testa elif flor jogador 1"""
    flor.estado_atual = ""
    jogador.flor = True
    jogador2.flor = False
    jogador.pontos = 5
    flor.pedir_flor(1, jogador, jogador2, interface_mock)
    assert flor.estado_atual == "Flor"
    assert flor.quem_venceu_flor == 1
    assert jogador.pontos == 8
    assert jogador2.pontos == 6

    """Testa elif flor jogador 2"""
    flor.estado_atual = ""
    jogador.flor = False
    jogador2.flor = True
    jogador2.pontos = 2
    flor.pedir_flor(2, jogador, jogador2, interface_mock)
    assert flor.estado_atual == "Flor"
    assert flor.quem_venceu_flor == 2
    assert jogador2.pontos == 5
    assert jogador.pontos == 8

    """Testa mostrar vencedor flor"""
    interface_mock.mostrar_vencedor_flor.assert_called_once_with

def test_contraflor(flor, jogador, jogador2, monkeypatch):
    """Testa jogador 1 vence contraflor"""
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 27)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor(1, jogador, jogador2)
    assert flor.quem_venceu_flor == 1
    assert jogador.pontos == 6
    assert jogador2.pontos == 0

    """Testa jogador 2 vence contraflor"""
    jogador.pontos = 0
    jogador2.pontos = 0
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 25)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor(1, jogador, jogador2)
    assert flor.quem_venceu_flor == 2
    assert jogador.pontos == 0
    assert jogador2.pontos == 6

    """Testa empate contraflor"""
    jogador.pontos = 6
    jogador2.pontos = 0
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 26)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor(1, jogador, jogador2)
    assert flor.quem_venceu_flor == 1
    assert jogador.pontos == 12
    assert jogador2.pontos == 0

def test_contraflor_resto(flor, jogador, jogador2, monkeypatch):
    """Testa valor envido = valor flor """
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 27)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor_resto(1, jogador, jogador2)
    assert flor.valor_envido == flor.valor_flor
    assert flor.quem_venceu_flor == 1
    assert jogador.pontos == 3
    assert jogador2.pontos == 0

    """Testa jogador 2 vence contraflor e resto"""
    jogador.pontos = 0
    jogador2.pontos = 0
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 25)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor_resto(1, jogador, jogador2)
    assert flor.quem_venceu_flor == 2
    assert jogador.pontos == 0
    assert jogador2.pontos == 3

    """Testa empate contraflor e resto"""
    jogador.pontos = 9
    jogador2.pontos = 0
    monkeypatch.setattr(jogador, "retorna_pontos_envido", lambda: 26)
    monkeypatch.setattr(jogador2, "retorna_pontos_envido", lambda: 26)
    flor.contraflor_resto(1, jogador, jogador2)
    assert flor.quem_venceu_flor == 1
    assert jogador.pontos == 12
    assert jogador2.pontos == 0

def test_decisao_jogador(flor, monkeypatch):
    flor.estado_atual = "Flor"
    """Testa decisão False"""""
    monkeypatch.setattr("builtins.input", lambda _: "0")
    resultado = flor.decisao_jogador()
    assert resultado == False

    """Testa decisão True"""""
    monkeypatch.setattr("builtins.input", lambda _: "1")
    resultado = flor.decisao_jogador()
    assert resultado == True

    """Testa entrada inválida seguida de válida"""""
    inputs = iter(["3", "-1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    resultado = flor.decisao_jogador()
    assert resultado == True

def test_resetar_flor(flor):
    flor.estado_atual = "Flor"
    flor.quem_pediu_flor = 1
    flor.quem_pediu_contraflor = 2
    flor.quem_pediu_contraflor_resto = 1
    flor.quem_venceu_flor = 2
    flor.valor_flor = 6
    flor.resetar_flor()
    assert flor.estado_atual == ""
    assert flor.quem_pediu_flor == 0
    assert flor.quem_pediu_contraflor == 0
    assert flor.quem_pediu_contraflor_resto == 0
    assert flor.quem_venceu_flor == 0
    assert flor.valor_flor == 3
