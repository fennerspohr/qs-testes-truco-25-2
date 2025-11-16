"""Testes de métodos da classe Envido"""

import sys
import pytest
from unittest.mock import patch
sys.path.append('../qs-testes-truco-25-2')

from truco.envido import Envido
from truco.interface import Interface

@pytest.fixture
def envido():
    return Envido()

def test_inverter_jogador_bloqueado(envido):
    """Testa se o jogador bloqueado é invertido"""
    envido.jogador_bloqueado = 1
    envido.inverter_jogador_bloqueado()
    assert envido.jogador_bloqueado == 2
    envido.inverter_jogador_bloqueado()
    assert envido.jogador_bloqueado == 1

def test_inicializar_jogador_bloqueado(envido):
    """Testa se o jogador é bloqueado corretamente"""
    envido.inicializar_jogador_bloqueado(1)
    assert envido.jogador_bloqueado == 1

def test_controlador_envido(envido,dados, cbr, jogador, jogador2, mocker):
    """Testa se os métodos corretos são chamados"""
    #estado_atual !=0 ou tipo == estado_atual
    assert envido.controlador_envido(cbr, dados, 0, 1, jogador, jogador2, Interface()) == None
    envido.estado_atual = 1
    assert envido.controlador_envido(cbr, dados, 0, 1, jogador, jogador2, Interface()) == None
    # quem_pediu = jogador_bloqueado
    envido.estado_atual = 0
    assert envido.controlador_envido(cbr, dados, 1, 0, jogador, jogador2, Interface()) == None
    # else
    envido.jogador_bloqueado = 2
    method1_mock = mocker.patch("truco.envido.Envido.inicializar_jogador_bloqueado")
    method2_mock = mocker.patch("truco.envido.Envido.definir_pontos_jogadores")
    method3_mock = mocker.patch("truco.envido.Envido.envido")
    method4_mock = mocker.patch("truco.envido.Envido.real_envido")
    method5_mock = mocker.patch("truco.envido.Envido.falta_envido")
    method6_mock = mocker.patch("truco.interface.Interface.mostrar_vencedor_envido")


    envido.controlador_envido(cbr, dados, 6, 1, jogador, jogador2, Interface())
    method1_mock.assert_called_with(1)
    method2_mock.assert_called_with(jogador, jogador2)
    #tipo 6
    method3_mock.assert_called_with(cbr, 1, jogador, jogador2)
    #tipo 7
    envido.controlador_envido(cbr, dados, 7, 1, jogador, jogador2, Interface())
    method4_mock.assert_called_with(cbr, 1, jogador, jogador2)
    #tipo 8
    envido.controlador_envido(cbr,dados, 8, 1, jogador, jogador2, Interface())
    method5_mock.assert_called_with(cbr, 1, jogador, jogador2)
    #quem fugiu = 0
    method6_mock.assert_called_with(0, jogador.nome, 0, jogador2.nome, 0)

def test_envido(envido, cbr, jogador, jogador2, monkeypatch):
    """Testa se o envido é realizado corretamente"""

    #humano pediu envido
    with patch.object(envido,'avaliar_vencedor_envido') as mock:
        envido.envido(cbr, 1, jogador, jogador2)
    mock.assert_called_with(1, jogador, jogador2)
    #robo pediu envido
        #humano foge
    monkeypatch.setattr('builtins.input', lambda _: 0)
    envido.envido(cbr, 2, jogador, jogador2)
    assert jogador2.pontos == 1
    assert envido.quem_fugiu == 1
        #humano aceita
    monkeypatch.setattr('builtins.input', lambda _: 1)
    with patch.object(envido,'avaliar_vencedor_envido') as mock:
        envido.envido(cbr, 2, jogador, jogador2)
    mock.assert_called_with(2, jogador, jogador2)
        # humano pede real envido
    monkeypatch.setattr('builtins.input', lambda _: 2)
    envido.jogador_bloqueado = 1
    with patch.object(envido, 'real_envido') as mock:
        envido.envido(cbr, 2, jogador, jogador2)
    mock.assert_called_with(cbr, 2, jogador, jogador2)
        #humano pede falta envido
    monkeypatch.setattr('builtins.input', lambda _: 3)
    envido.jogador_bloqueado = 1
    with patch.object(envido, 'falta_envido') as mock:
        envido.envido(cbr, 2, jogador, jogador2)
    mock.assert_called_with(cbr, 2, jogador, jogador2)

def test_real_envido(envido, cbr, jogador, jogador2, mocker, monkeypatch):
    """Testa se o real envido é realizado corretamente"""
    method1_mock = mocker.patch('truco.bot.Bot.avaliar_envido')
    method1_mock.return_value = 1
    method2_mock = mocker.patch('truco.envido.Envido.avaliar_vencedor_envido')
    # humano pediu real envido
    envido.real_envido(cbr, 1, jogador, jogador2)
    method1_mock.assert_called_with(cbr, 7, 1,envido.jogador2_pontos)
    method2_mock.assert_called_with(1, jogador, jogador2)
    #robo pediu real envido
        # humano fugiu
    monkeypatch.setattr('builtins.input', lambda _: 0)
    envido.real_envido(cbr, 2, jogador, jogador2)
    assert jogador2.pontos == 2
    assert envido.quem_fugiu == 1
        # humano aceitou
    monkeypatch.setattr('builtins.input', lambda _: 1)
    envido.real_envido(cbr, 2, jogador, jogador2)
    method2_mock.assert_called_with(2, jogador, jogador2)
        # humano pediu falta envido
    envido.jogador_bloqueado = 2
    monkeypatch.setattr('builtins.input', lambda _: 2)
    with patch.object(envido, 'falta_envido') as mock:
        envido.real_envido(cbr, 2, jogador, jogador2)
    mock.assert_called_with(cbr, 1, jogador, jogador2)

def test_falta_envido(cbr, envido, jogador, jogador2, mocker, monkeypatch):
    """Testa se o falta envido é realizado corretamente"""
    method1_mock = mocker.patch('truco.bot.Bot.avaliar_envido')
    method1_mock.return_value = 1
    method2_mock = mocker.patch('truco.envido.Envido.avaliar_vencedor_falta_envido')
    # humano pediu falta envido
    envido.falta_envido(cbr, 1, jogador, jogador2)
    method1_mock.assert_called_with(cbr, 8, 1, envido.jogador2_pontos)
    method2_mock.assert_called_with(1, jogador, jogador2)
    # bot pediu falta envido
        # humano fugiu
    monkeypatch.setattr('builtins.input', lambda _: 0)
    retorno = envido.falta_envido(cbr, 2, jogador, jogador2)
    assert jogador2.pontos == 5
    assert envido.quem_fugiu == 1
    assert retorno == False
        # humano aceitou
    monkeypatch.setattr('builtins.input', lambda _: 1)
    envido.falta_envido(cbr, 2, jogador, jogador2)
    method2_mock.assert_called_with(2, jogador, jogador2)

def test_avaliar_vencedor_envido(envido, jogador, jogador2):
    """Testa se o vencedor do envido está sendo definido corretamente"""
    # humano >= robo
    envido.jogador1_pontos = 1
    envido.valor_envido = 1
    envido.avaliar_vencedor_envido(1, jogador, jogador2)
    assert jogador.pontos == 1
    assert envido.quem_venceu_envido == 1
    # robo > humano
    envido.jogador2_pontos = 2
    envido.avaliar_vencedor_envido(1, jogador, jogador2)
    assert jogador2.pontos == 1
    assert envido.quem_venceu_envido == 2

def test_avaliar_vencedor_falta_envido(envido, jogador, jogador2):
    """Testa se o vencedor do falta envido está sendo definido corretamente"""
    # humano >= robo
    envido.jogador1_pontos = 1
    envido.valor_envido = 1
    envido.avaliar_vencedor_falta_envido(1, jogador, jogador2)
    assert jogador.pontos == 1
    assert envido.quem_venceu_envido == 1
        # robo > humano
    envido.jogador2_pontos = 2
    envido.avaliar_vencedor_falta_envido(1, jogador, jogador2)
    assert jogador2.pontos == 1
    assert envido.quem_venceu_envido == 2

def test_definir_pontos_jogadores(envido, jogador, jogador2):
    """Testa se os pontos de envido dos jogadores estão sendo salvos corretamente"""
    jogador.envido = 5
    jogador2.envido = 7
    envido.definir_pontos_jogadores(jogador, jogador2)
    assert envido.jogador1_pontos == 5
    assert envido.jogador2_pontos == 7

def test_retornar_quem_fugiu(envido):
    """Testa se o jogador que fugiu do envido está sendo retornado corretamente"""
    envido.quem_fugiu = 2
    assert envido.retornar_quem_fugiu() == 2

def test_resetar(envido):
    envido.valor_envido = 12
    envido.estado_atual = 1
    envido.jogador_pediu_envido = 2
    envido.quem_real_envido = 1
    envido.quem_falta_envido = 1
    envido.quem_fugiu = 2
    envido.quem_venceu_envido = 2
    envido.jogador_bloqueado = 1
    envido.jogador1_pontos = 1
    envido.jogador2_pontos = 3
    envido.resetar()
    assert envido.valor_envido == 2
    assert envido.estado_atual == 0
    assert envido.jogador_pediu_envido == 0
    assert envido.quem_real_envido == 0
    assert envido.quem_falta_envido == 0
    assert envido.quem_fugiu == 0
    assert envido.quem_venceu_envido == 0
    assert envido.jogador_bloqueado == 0 
    assert envido.jogador1_pontos == 0
    assert envido.jogador2_pontos == 0
