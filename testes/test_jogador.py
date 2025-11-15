"""Testes de métodos da classe Jogador"""

import pytest
from truco.interface import Interface


def test__init__(jogador):
    """Testa a criação de instâncias da classe Jogador"""
    assert jogador.nome == "Testes"
    assert jogador.mao == []
    assert jogador.mao_rank == []
    assert jogador.pontos == 0
    assert jogador.rodadas == 0
    assert jogador.envido == 0 
    assert jogador.primeiro == False
    assert jogador.ultimo == False
    assert jogador.flor == False
    assert jogador.pediu_flor == False
    assert jogador.pediu_truco == False

def test_mostrar_opcoes(jogador, bastiao, capsys, espadao):
    """Testa todos os possíveis prints de opções"""
    jogador.mao = [bastiao, bastiao, bastiao]
    jogador.mostrar_opcoes(Interface())
    captured = capsys.readouterr()
    # Print quando tem 3 cartas de mesmo naipe na mão e ainda não chamou truco nem flor
    assert '[4] Truco' in captured.out
    assert f'[6] Envido\n[7] Real Envido\n[8] Falta Envido' in captured.out
    assert '[5] Flor' in captured.out
    assert jogador.flor == True
    assert '[9] Ir ao baralho' in captured.out
    # Print quando tem 3 cartas de mesmo naipe na mão e já chamou truco e tem flor
    jogador.pediu_truco = True
    jogador.mostrar_opcoes(Interface())
    captured = capsys.readouterr()
    assert '[4] Truco'  not in captured.out
    assert f'[6] Envido\n[7] Real Envido\n[8] Falta Envido' in captured.out
    assert '[5] Flor' not in captured.out
    assert '[9] Ir ao baralho' in captured.out
    # Print quando tem 3 cartas de naipes diferentes na mão 
    jogador.mao = [espadao, bastiao, bastiao]
    jogador.flor = False
    jogador.mostrar_opcoes(Interface())
    captured = capsys.readouterr()
    assert '[5] Flor' not in captured.out
    assert f'[6] Envido\n[7] Real Envido\n[8] Falta Envido' in captured.out
    assert '[9] Ir ao baralho' in captured.out
    assert jogador.flor == False
    # Print quando tem menos de 3 cartas e não chamou truco
    jogador.mao = [espadao, bastiao]
    jogador.pediu_truco = False
    jogador.mostrar_opcoes(Interface())
    captured = capsys.readouterr()
    assert f'[6] Envido\n[7] Real Envido\n[8] Falta Envido' not in captured.out
    assert '[9] Ir ao baralho' in captured.out
    assert '[4] Truco' in captured.out
    # Print com menos de 2 cartas
    jogador.mao = [bastiao]
    jogador.mostrar_opcoes(Interface())
    captured = capsys.readouterr()
    assert '[4] Truco'  not in captured.out
    assert '[9] Ir ao baralho' in captured.out

def test_criar_mao(baralho, jogador):
    """Verifica se o jogador recebe o número correto de cartas e se sua pontuação é calculada corretamente"""
    expectedCards = [baralho.cartas[len(baralho.cartas)-1], baralho.cartas[len(baralho.cartas)-2], baralho.cartas[len(baralho.cartas)-3]]
    jogador.criar_mao(baralho)
    assert len(jogador.mao) == 3
    assert jogador.envido == jogador.calcula_envido(expectedCards)

def test_jogar_carta(jogador, espadao, bastiao, carta_alta_ouro):
    """Testa se a carta correta é jogada e se a carta sai da mão do jogador"""
    jogador.mao = [espadao, bastiao, carta_alta_ouro]
    jogada = jogador.jogar_carta(1)
    assert jogada == bastiao
    assert bastiao not in jogador.mao
    assert len(jogador.mao) == 2

def test_mostrar_mao(jogador, bastiao, espadao, carta_alta_ouro, capsys):
    """Testa se a mão do jogador é exibida corretamente"""
    jogador.mao = [bastiao, espadao, carta_alta_ouro]
    bastiao.exibir_carta(0)
    espadao.exibir_carta(1)
    carta_alta_ouro.exibir_carta(2)
    expected = capsys.readouterr()
    jogador.mostrar_mao(Interface())
    captured = capsys.readouterr()
    assert captured.out == expected.out

def test_adicionar_pontos(jogador):
    """Testa se os pontos são adicionados corretamente"""
    jogador.adicionar_pontos(5)
    assert jogador.pontos == 5
    jogador.adicionar_pontos(2)
    assert jogador.pontos == 7

def test_adicionar_rodada(jogador):
    """Testa se a adição de rodadas está correta"""
    jogador.adicionar_rodada()
    assert jogador.rodadas == 1
    jogador.adicionar_rodada()
    assert jogador.rodadas == 2

def test_checa_mao(jogador, espadao, bastiao):
    """Testa se as cartas são retornadas corretamente"""
    cartas = [espadao, bastiao, bastiao]
    jogador.mao = cartas
    assert jogador.checa_mao() == cartas

def test_calcula_envido(jogador, carta_baixa_copas, carta_alta_ouro, carta_baixa_ouro, espadao):
    """Testa se o cálculo de envido está correto"""
    # Três cartas do mesmo naipe, com um valor possível de envido
    mao = [carta_alta_ouro, carta_alta_ouro, carta_alta_ouro]
    assert jogador.calcula_envido(mao) == 20 + carta_alta_ouro.retornar_pontos_envido(carta_alta_ouro) * 2

    # Três cartas do mesmo naipe. com dois valores possíveis de envido
    mao = [carta_alta_ouro, carta_alta_ouro, carta_baixa_ouro]
    assert jogador.calcula_envido(mao) == 20 + carta_alta_ouro.retornar_pontos_envido(carta_alta_ouro) + carta_baixa_ouro.retornar_pontos_envido(carta_baixa_ouro)

    # Três cartas de naipes diferentes
    mao = [carta_baixa_ouro, espadao, carta_baixa_copas]
    assert jogador.calcula_envido(mao) == carta_baixa_copas.retornar_pontos_envido(carta_baixa_copas)

def test_checa_flor(jogador, espadao, bastiao):
    """Testa se o método reconhece flor corretamente"""
    # Três cartas do mesmo naipe
    jogador.mao = [espadao, espadao, espadao]
    assert jogador.checa_flor() == True
    # Duas cartas iguais e uma diferente
    jogador.mao = [espadao, espadao, bastiao]
    assert jogador.checa_flor() == False

def test_retorna_pontos_envido(jogador):
    """Testa se a pontuação total de envido da mão é retornada corretamente"""
    jogador.envido = 3
    assert jogador.retorna_pontos_envido() == 3

def test_retorna_pontos_totais(jogador):
    """Testa se a pontuação total do jogador é retornada corretamente"""
    jogador.pontos = 3
    assert jogador.retorna_pontos_totais() == 3

def test_resetar(jogador):
    """Testa se o jogador é resetado corretamente"""
    jogador.rodads = 1
    jogador.mao = [2]
    jogador.flor = True
    jogador.pediu_truco = True
    jogador.resetar()
    assert jogador.rodadas == 0
    assert jogador.mao == []
    assert jogador.flor == False
    assert jogador.pediu_truco == False
    