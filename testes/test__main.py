"""Testes de métodos da classe Main"""

import sys
import pytest
from unittest.mock import MagicMock
sys.path.append('../qs-testes-truco-25-2')

from truco.logica import reiniciarJogo, turno_do_humano, turno_do_bot, main
from truco.interface import Interface
from truco.envido import Envido
from truco.truco import Truco
from truco.bot import Bot
from truco.jogo import Jogo

@pytest.fixture
def envido():
    return Envido()

@pytest.fixture
def truco():
    return Truco()

@pytest.fixture
def interface():
    return Interface()

@pytest.fixture
def jogo():
    return Jogo()

def test_turno_do_humano1(monkeypatch, mocker, interface, baralho,jogador, jogadorBot2, cbr, envido, dados, truco, flor):
    """Testa as funcionalidades do turno do jogador humano"""
###teste 1
    # jogador1 com 3 cartas na mao e jogador2 envido
        # bot aceita envido (1)
    #while
        # jogador 1 tem 3 cartas E escolheu 6,7,8 E jogador2 tem flor
        # aqui carta escolhida = -1; bot pediu flor pra bloquear envido
        # ok print selecione um valor valido
        # escolhe uma carta normal pra jogar

    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    jogadorBot2.envido = True
    jogadorBot2.flor = True
    method1_mock = mocker.patch.object(jogadorBot2, 'avaliar_envido')
    method1_mock.return_value = True
    method2_mock = mocker.patch.object(jogador, 'mostrar_opcoes')
    method3_mock = mocker.patch.object(envido, 'controlador_envido')
    method4_mock = mocker.patch.object(flor, 'pedir_flor')
    inputs = iter([6, 1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method1_mock.assert_called_with(cbr, 'Envido',2, jogador.pontos)
    method2_mock.assert_called_with(interface)
    method3_mock.assert_called_with(cbr, dados, 6, 2, jogador, jogadorBot2, interface)
    method4_mock.assert_called_with(1, jogador, jogadorBot2, interface)
    assert retorno not in carta1
###teste 2
    # jogador1 com 3 cartas na mao e jogador2 envido
        # bot recusa envido (0)
    #while
        #jogador chama truco
        #chamou truco false
    method1_mock.return_value = False
    method5_mock = mocker.patch.object(truco, 'controlador_truco')
    method5_mock.return_value = False
    method6_mock = mocker.patch.object(truco, 'retornar_valor_aposta')
    inputs = iter([4])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method1_mock.assert_called_with(cbr, 'Envido',2, jogador.pontos)
    method5_mock.assert_called_with(cbr, dados, 1, jogador, jogadorBot2)
    method6_mock.assert_called_with()
    assert retorno == -1

###teste 3
    #while
        #jogador chama truco
        #chamou truco
        #jogou uma carta normal
    #carta jogada
    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    method4_mock.return_value = True
    inputs = iter([4, 1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method5_mock.assert_called_with(cbr, dados, 1, jogador, jogadorBot2)
    assert retorno not in carta1

def test_turno_do_humano2(monkeypatch, mocker, interface, jogador, baralho, jogadorBot2, cbr, dados, flor, envido):

###teste 4
    #while
        # jogador tem 3 cartas e chama flor
        #joga uma carta normak
    #carta jogada
    jogadorBot2.envido = False
    method1_mock = mocker.patch.object(interface, 'border_msg')
    method2_mock = mocker.patch.object(flor, 'pedir_flor')
    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    jogador.flor = True
    inputs = iter([5, 1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method2_mock.assert_called_with(1, jogador, jogadorBot2, interface)
    method1_mock.assert_called_with(f"Jogador 1 - {jogador.nome}: {jogador.pontos} Pontos Acumulados\nJogador 2 - {jogadorBot2.nome}: {jogadorBot2.pontos} Pontos Acumulados")
    assert retorno not in carta1

def teste_turno_do_humano3(monkeypatch, mocker, interface, jogador, baralho, jogadorBot2, cbr, dados, flor, envido):
###teste 5
    #while
        # jogador pede envido (jogador2 nao pediu, tem 3 cartas)
            #pediu envido
        # tentar pedir envido de novo
        #jogar carta normal
    method3_mock = mocker.patch.object(envido, 'controlador_envido')
    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    jogador.flor = False
    jogadorBot2.pediu_flor =  False
    inputs = iter([6, 6,1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method3_mock.assert_called_with(cbr, dados, 6, 1, jogador, jogadorBot2, interface)
    assert retorno not in carta1

def teste_turno_do_humano4(monkeypatch, mocker, interface, jogador, baralho, jogadorBot2, cbr, dados, flor, envido):
###teste 6
    #while
        # jogador pede envido (jogador2 nao pediu, tem 3 cartas)
            #pediu real envido
        #jogar carta normal
    method3_mock = mocker.patch.object(envido, 'controlador_envido')
    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    jogador.flor = False
    jogadorBot2.pediu_flor =  False
    inputs = iter([7,1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method3_mock.assert_called_with(cbr, dados, 7, 1, jogador, jogadorBot2, interface)
    assert retorno not in carta1

def teste_turno_do_humano5(monkeypatch, mocker, interface, jogador, baralho, jogadorBot2, cbr, dados, flor, envido):
###teste 7
    #while
        # jogador pede envido (jogador2 nao pediu, tem 3 cartas)
            #pediu falta envido
        #jogar carta normal
    method3_mock = mocker.patch.object(envido, 'controlador_envido')
    jogador.criar_mao(baralho)
    carta1 = jogador.mao
    jogador.flor = False
    jogadorBot2.pediu_flor =  False
    inputs = iter([8,1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method3_mock.assert_called_with(cbr, dados, 8, 1, jogador, jogadorBot2, interface)
    assert retorno not in carta1

def teste_turno_do_humano5(monkeypatch, mocker, interface, jogador, baralho, jogadorBot2, cbr, dados, flor, envido, truco):
###teste 8
    #while
        #ir ao baralho (9)
###teste 9
    #while
        #selecionar valor inválido
    method1_mock = mocker.patch.object(jogadorBot2, 'adicionar_pontos')
    method2_mock = mocker.patch.object(truco, 'retornar_valor_aposta')
    method2_mock.return_value = 1
    jogador.criar_mao(baralho)
    jogador.flor = False
    inputs = iter([10,9])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    retorno = turno_do_humano(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    method1_mock.assert_called_with(1)
    method2_mock.assert_called_with()
    assert retorno == -1

def test_turno_do_bot1(mocker, interface, jogador, jogadorBot2, cbr, dados, truco, flor, envido, espadao, baralho):
###teste 1
    # bot tem 3 cartas e tem carta do jogador
        #enriquecer bot
    #while
        #carta escolhida = 5 (flor)
        #jogador2 não pediu flor e jogador1 tem 3 cartas
            #pede flor
            #joga carta normal
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    jogadorBot2.pediu_flor = False
    jogadorBot2.flor = False
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [5,1]
    mocked_dependency2 = mocker.patch('truco.bot.Bot.checa_flor')
    mocked_dependency2.return_value = True
    mocked_dependency3 = mocker.patch('truco.cbr.Cbr.flor')
    mocked_dependency3.return_value = True
    mocked_dependency.return_value = [5,1]
    method1_mock = mocker.patch.object(flor, 'pedir_flor')
    method2_mock = mocker.patch.object(interface, 'border_msg')
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    mocked_dependency.assert_called_with(cbr, truco)
    method1_mock.assert_called_with(2, jogador, jogadorBot2, interface)
    method2_mock.assert_called_with(f"Jogador 1 - {jogador.nome}: {jogador.pontos} Pontos Acumulados\nJogador 2 - {jogadorBot2.nome}: {jogadorBot2.pontos} Pontos Acumulados")
    assert retorno not in cartas
def test_turno_do_bot2(mocker, interface, jogador, jogadorBot2, cbr, dados, truco, flor, envido, espadao, baralho):
###teste 2
    #while
        # chamou truco (4)
        #false
    jogadorBot2.criar_mao(baralho)
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [4]
    method1_mock = mocker.patch.object(truco, 'controlador_truco')
    method1_mock.return_value = False
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(cbr, dados, 2, jogador, jogadorBot2)
    assert retorno == -1
###teste 3
    #while
        #chamou truco
        #aceitou
        #joga carta normal
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    mocked_dependency.side_effect = [4, 1]
    method1_mock.return_value = True
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(cbr, dados, 2, jogador, jogadorBot2)
    assert retorno not in cartas

def test_turno_do_bot3(mocker, interface, jogador, jogadorBot2, cbr, dados, truco, flor, envido, espadao, baralho):
###teste 4
    #while
        # jogador 1 pediu_flor false e jogador2 pediu_flor false
        # pede envido
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    jogadorBot2.pediu_flor = False
    jogador.pediu_flor = False
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [6,1]
    method1_mock = mocker.patch.object(envido, 'controlador_envido')
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(cbr, dados, 6, 1, jogador, jogadorBot2, interface)
    assert retorno not in cartas

###teste 5
    #while
        # jogador 1 pediu_flor true e jogador2 pediu_flor false
        # pede envido
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [6,1]
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    jogadorBot2.pediu_flor = False
    jogador.pediu_flor = True
    method1_mock.reset_mock()
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    assert method1_mock.call_count == 0
    assert retorno not in cartas
###teste 6
    #while
        # pede real envido 7
    jogadorBot2 = Bot("bot")
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    jogadorBot2.pediu_flor = False
    jogador.pediu_flor = False
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [7,1]
    method1_mock.reset_mock()
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(cbr, dados, 7, 1, jogador, jogadorBot2, interface)
    assert retorno not in cartas

###teste 7
    #while
        #pede real envido 8
    jogadorBot2.criar_mao(baralho)
    cartas = jogadorBot2.mao
    jogadorBot2.pediu_flor = False
    jogador.pediu_flor = False
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    mocked_dependency.side_effect = [8,1]
    method1_mock.reset_mock()
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(cbr, dados, 8, 1, jogador, jogadorBot2, interface)
    assert retorno not in cartas

def test_turno_do_bot4(mocker, interface, jogador, jogadorBot2, cbr, dados, truco, flor, envido, espadao, baralho):
###teste 8
    #while
        #seleciona valor invalido
        #vai ao baralho
    jogadorBot2.pediu_flor = False
    mocked_dependency = mocker.patch('truco.bot.Bot.jogar_carta')
    method1_mock = mocker.patch.object(jogador, 'adicionar_pontos')
    method2_mock = mocker.patch.object(envido, 'controlador_envido')
    mocked_dependency.side_effect = [10, 7]

    jogador.pediu_flor = True
    method1_mock = mocker.patch.object(jogador, 'adicionar_pontos')
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(1)
    assert retorno == -1
    jogador.pediu_flor = False
    retorno = turno_do_bot(espadao, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    method1_mock.assert_called_with(1)
    assert retorno == -1
    
def test_main1(mocker, interface, jogador, jogadorBot2, jogo, baralho, cbr, dados, truco, flor, envido):
###teste 1
    #while
        #jogador primeiro true
        #carta jogador == -1
        #jogador pontos == 12
    jogador.primeiro = True
    jogador.pontos = 12
    turno_humano_mock = mocker.patch('truco.logica.turno_do_humano')
    turno_humano_mock.return_value = -1
    mostrar_placar_total_jogador_fugiu_mock = mocker.patch.object(interface, 'mostrar_placar_total_jogador_fugiu')
    mostrar_ganhador_jogo_mock = mocker.patch.object(interface, 'mostrar_ganhador_jogo')
    main(jogo, baralho, cbr, interface, dados, truco, flor, envido, jogador, jogadorBot2)
    turno_humano_mock.assert_called_with(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    mostrar_placar_total_jogador_fugiu_mock.assert_called_with(jogador, jogador.nome, jogador.pontos, jogadorBot2.nome, jogadorBot2.pontos)
    mostrar_ganhador_jogo_mock.assert_called_with(jogador.nome)

def test_main2(mocker, interface, jogador, jogadorBot2, jogo, baralho, cbr, dados, truco, flor, envido):
### teste 2
    #while
        #jogador primeiro true
        #carta jogador != -1
        #carta bot = -1
        #bot pontos = 12
    jogador.primeiro = True
    jogadorBot2.pontos = 12
    turno_humano_mock = mocker.patch('truco.logica.turno_do_humano')
    turno_humano_mock.return_value = 1
    mostrar_carta_jogada_mock = mocker.patch.object(interface, 'mostrar_carta_jogada')
    turno_bot_mock = mocker.patch('truco.logica.turno_do_bot')
    turno_bot_mock.return_value = -1
    mostrar_placar_total_jogador_fugiu_mock = mocker.patch.object(interface, 'mostrar_placar_total_jogador_fugiu')
    mostrar_ganhador_jogo_mock = mocker.patch.object(interface, 'mostrar_ganhador_jogo')
    main(jogo, baralho, cbr, interface, dados, truco, flor, envido, jogador, jogadorBot2)
    turno_humano_mock.assert_called_with(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    mostrar_carta_jogada_mock.assert_called_with(jogador.nome, 1)
    turno_bot_mock.assert_called_with(1, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    mostrar_placar_total_jogador_fugiu_mock.assert_called_with(jogadorBot2, jogador.nome, jogador.pontos, jogadorBot2.nome, jogadorBot2.pontos)
    mostrar_ganhador_jogo_mock.assert_called_with(jogadorBot2.nome)

### teste 3
    #while
        #jogador primeiro true
        #carta jogador != 1
        #carta bot != 1
        #jogador rodadas = 2
        #reinicia
    jogador.primeiro = True
    jogador.rodadas = 2
    jogador.pontos = 11
    turno_humano_mock = mocker.patch('truco.logica.turno_do_humano')
    turno_humano_mock.return_value = 1
    mostrar_carta_jogada_mock = mocker.patch.object(interface, 'mostrar_carta_jogada')
    turno_bot_mock = mocker.patch('truco.logica.turno_do_bot')
    turno_bot_mock.return_value = 1
    verificar_ganhador_mock = mocker.patch.object(jogo, 'verificar_ganhador')
    verificar_ganhador_mock.return_value = 1
    quem_joga_primeiro_mock = mocker.patch.object(jogo, 'quem_joga_primeiro')
    adicionar_rodada_mock = mocker.patch.object(jogo, 'adicionar_rodada')
    adicionar_rodada_mock.return_value = 1
    enriquecer_bot_mock = mocker.patch.object(jogadorBot2, 'enriquecer_bot')
    retornar_valor_aposta_mock = mocker.patch.object(truco, 'retornar_valor_aposta')
    retornar_valor_aposta_mock.return_value = 1
    adicionar_pontos_mock = mocker.patch.object(jogador, 'adicionar_pontos')
    mostrar_ganhador_rodada_mock = mocker.patch.object(interface, 'mostrar_ganhador_rodada')
    reinciarJogo_mock = mocker.patch('truco.logica.reiniciarJogo')
    main(jogo, baralho, cbr, interface, dados, truco, flor, envido, jogador, jogadorBot2)
    turno_humano_mock.assert_called_with(jogadorBot2, jogador, cbr, interface, envido, dados, truco, flor)
    assert mostrar_carta_jogada_mock.call_count == 2
    turno_bot_mock.assert_called_with(1, jogadorBot2, dados, cbr, truco, jogador, flor, interface, envido)
    verificar_ganhador_mock.assert_called_with(1, 1, interface)
    quem_joga_primeiro_mock.assert_called_with(jogador, jogadorBot2,1, 1, 1)
    adicionar_rodada_mock.assert_called_with(jogador, jogadorBot2, 1, 1, 1)
    assert enriquecer_bot_mock.call_count == 2
    retornar_valor_aposta_mock.assert_called_with()
    adicionar_pontos_mock.assert_called_with(1)
    mostrar_ganhador_rodada_mock.assert_called_with(jogador.nome)
    reinciarJogo_mock.assert_called_with(dados, jogador, jogadorBot2, baralho, envido, truco)

def test_reiniciarJogo(mocker,dados, jogador, jogadorBot2, baralho, envido, truco):
    finalizar_partida_mock = mocker.patch.object(dados, 'finalizar_partida')
    resetar1_mock = mocker.patch.object(jogador, 'resetar')
    resetar2_mock = mocker.patch.object(jogadorBot2, 'resetar')
    resetar_baralho_mock = mocker.patch.object(baralho, 'resetar')
    criar_baralho_mock = mocker.patch.object(baralho, 'criar_baralho')
    embaralhar_mock = mocker.patch.object(baralho, 'embaralhar')
    criar_mao1_mock = mocker.patch.object(jogador, 'criar_mao')
    criar_mao2_mock = mocker.patch.object(jogadorBot2, 'criar_mao')
    resetar_envido_mock = mocker.patch.object(envido, 'resetar')
    resetar_truco_mock = mocker.patch.object(truco, 'resetar')
    reiniciarJogo(dados, jogador, jogadorBot2, baralho, envido, truco)
    finalizar_partida_mock.assert_called_once()
    resetar1_mock.assert_called_once()
    resetar2_mock.assert_called_once()
    resetar_baralho_mock.assert_called_once()
    criar_baralho_mock.assert_called_once()
    embaralhar_mock.assert_called_once()
    criar_mao1_mock.assert_called_with(baralho)
    criar_mao2_mock.assert_called_with(baralho)
    resetar_envido_mock.assert_called_once()
    resetar_truco_mock.assert_called_once()
