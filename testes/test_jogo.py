"""Testes de métodos da classe Jogo"""

import sys
import pytest
from unittest.mock import patch

sys.path.append('../qs-testes-truco-25-2')

from truco.jogo import Jogo
from truco.interface import Interface
from truco.pontos import MANILHA, CARTAS_VALORES

@pytest.fixture
def jogo():
    return Jogo()

def test_criar_jogador(jogo, baralho):
    """Testa a criação de um jogador humano"""
    jog = jogo.criar_jogador("Teste", baralho)
    assert jog.nome == "Teste"

def test_criar_bot(jogo, baralho):
    """Testa a criação do jogador bot"""
    b = jogo.criar_bot("Bot", baralho)
    assert b.nome == "Bot"

def test_verificar_ganhador(jogo, carta_alta_ouro, carta_baixa_copas, mocker):
    """Testa se o método de verificação é chamado corretamente"""
    interface = Interface()
    ganhador = jogo.verificar_ganhador(carta_alta_ouro, carta_baixa_copas, interface)
    assert ganhador == carta_alta_ouro
    method1_mock = mocker.patch("truco.interface.Interface.mostrar_carta_ganhadora")
    ganhador = jogo.verificar_ganhador(carta_alta_ouro, carta_baixa_copas, interface)
    method1_mock.assert_called_with(ganhador)
    method2_mock = mocker.patch("truco.jogo.Jogo.verificar_carta_vencedora")
    ganhador = jogo.verificar_ganhador(carta_alta_ouro, carta_baixa_copas, interface)
    method2_mock.assert_called_with(carta_alta_ouro, carta_baixa_copas)

def test_adicionar_rodada(jogo, jogador, jogadorBot2, espadao, carta_baixa_copas, bastiao):
    """Testa se as rodadas são adicionadas corretamente aos jogadores"""
    # humano ganhador
    with patch.object(jogador, 'adicionar_rodada') as mock:
        retorno = jogo.adicionar_rodada(jogador, jogadorBot2, espadao, carta_baixa_copas, espadao)
    mock.assert_called_with()
    assert retorno == 1
    # bot ganhador
    with patch.object(jogadorBot2, 'adicionar_rodada') as mock:
        retorno = jogo.adicionar_rodada(jogador, jogadorBot2, espadao, carta_baixa_copas, carta_baixa_copas)
    mock.assert_called_with()
    assert retorno == 2
    assert jogo.adicionar_rodada(jogador, jogadorBot2, espadao, carta_baixa_copas, bastiao) == "Erro"

def test_quem_joga_primeiro(jogo, jogador, jogadorBot2, espadao, bastiao):
    """Testa se o primeiro a jogar é definido corretamente"""
    jogo.quem_joga_primeiro(jogador, jogadorBot2, espadao, bastiao, espadao)
    assert jogador.primeiro == True
    assert jogadorBot2.primeiro == False
    jogo.quem_joga_primeiro(jogador, jogadorBot2, espadao, bastiao, bastiao)
    assert jogador.primeiro == False
    assert jogadorBot2.primeiro == True

def test_quem_inicia_rodada(jogo, jogador, jogadorBot2):
    """Testa se quem inicia a rodada é definido corretamente"""
    jogador.ultimo = True
    jogo.quem_inicia_rodada(jogador, jogadorBot2)
    assert jogador.ultimo == False
    assert jogadorBot2.ultimo == True
    assert jogador.primeiro == True
    assert jogadorBot2.primeiro == False
    jogo.quem_inicia_rodada(jogador, jogadorBot2)
    assert jogadorBot2.ultimo == False
    assert jogador.primeiro == False
    assert jogadorBot2.primeiro == True
    jogador.ultimo = None
    jogador.primeiro = None
    jogadorBot2.ultimo = None
    jogadorBot2.primeiro = None
    jogador.rodadas = 1
    jogo.quem_inicia_rodada(jogador, jogadorBot2)
    assert jogador.primeiro == None
    assert jogadorBot2.primeiro == None
    assert jogador.ultimo == None
    assert jogadorBot2.ultimo == None

def test_verificar_carta_vencedora(jogo, espadao, bastiao, carta_alta_ouro, carta_baixa_copas, carta_baixa_ouro):
    """Testa se a verificação de carta vencedora é feita corretamente"""
    # duas manilhas de valores diferentes
    assert jogo.verificar_carta_vencedora(espadao, bastiao) == espadao
    # duas manilhas iguais
    assert jogo.verificar_carta_vencedora(espadao, espadao) == espadao
    # uma manilha
    assert jogo.verificar_carta_vencedora(carta_baixa_ouro, bastiao) == bastiao
    # cartas normais diferentes
    assert jogo.verificar_carta_vencedora(carta_baixa_ouro, carta_alta_ouro) == carta_alta_ouro
    # cartas normais iguais
    assert jogo.verificar_carta_vencedora(carta_baixa_ouro, carta_baixa_copas) == carta_baixa_copas

def test_jogador_fugiu(jogo, jogador, jogadorBot2):
    """Testa se a ordem de jogadas é resetada corretamente quando um jogador foge"""
    jogo.jogador_fugiu(jogador, jogador, jogadorBot2, 0)
    assert jogador.primeiro == True
    assert jogadorBot2.primeiro == False
