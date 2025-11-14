"""Testes de métodos da classe Bot"""
import sys
import random
import pytest
from unittest.mock import MagicMock
sys.path.append('../qs-testes-truco-25-2')
from truco.baralho import Baralho
from truco.bot import Bot
from truco.carta import Carta

@pytest.fixture
def bot():
    return Bot("Bot Teste")

@pytest.fixture
def bot_indices():
    b = Bot("Bot Índices")
    b.indices = [0, 1, 2]
    b.mao_rank = [10, 20, 30]
    b.pontuacao_cartas = [5, 15, 25]
    return b

@pytest.fixture
def bot_reset():
    b = Bot("Bot Reset")
    b.mao = [Carta(1, "OUROS"), Carta(2, "ESPADAS"), Carta(3, "COPAS")]
    b.mao_rank = [10, 20, 30]
    b.indices = [0, 1, 2]
    b.pontuacao_cartas = [5, 15, 25]
    b.qualidade_mao = 7
    b.rodadas = 3
    b.envido = 1
    b.rodada = 1
    b.flor = True
    b.pediu_flor = True
    b.pediu_truco = True
    return b

@pytest.fixture(params=[0, 1, 2])
def i(request):
    return request.param

@pytest.fixture(params=[0, 1, 2])
def pontos(request):
    return request.param

@pytest.fixture
def baralho():
    b = Baralho()
    b.embaralhar()
    return b

@pytest.fixture
def carta_alta_ouro():
    return Carta(3, "OUROS")

@pytest.fixture
def carta_baixa_ouro():
    return Carta(4, "OUROS")

@pytest.fixture
def carta_mock():
    return MagicMock(spec=Carta)

@pytest.fixture
def carta2_mock():
    return MagicMock(spec=Carta)

@pytest.fixture
def carta3_mock():
    return MagicMock(spec=Carta)

@pytest.fixture
def dados_mock():
    mock = MagicMock()
    return mock

@pytest.fixture
def cbr_mock():
    mock = MagicMock()
    return mock

@pytest.fixture
def truco_mock():
    mock = MagicMock()
    return mock

@pytest.fixture
def mao():
    return [Carta(1, "BASTIOS"), Carta(7, "OUROS"), Carta(3, "OUROS")]

@pytest.fixture
def mao_mock(carta_mock, carta2_mock, carta3_mock):
    return [carta_mock, carta2_mock, carta3_mock]

@pytest.fixture
def mao_com_flor():
    return [Carta(7, "OUROS"), Carta(6, "OUROS"), Carta(3, "OUROS")]


def test__init__(bot):
    assert bot.nome == "Bot Teste"
    assert bot.mao == []
    assert bot.mao_rank == []
    assert bot.indices == []
    assert bot.pontuacao_cartas == []
    assert bot.qualidade_mao == 0
    assert bot.pontos == 0
    assert bot.rodadas == 0
    assert bot.envido == 0
    assert bot.rodada == 1
    assert bot.primeiro is False
    assert bot.ultimo is False
    assert bot.flor is False
    assert bot.pediu_flor is False
    assert bot.pediu_truco is False 

def test_criar_mao(bot, baralho):
    """Testa se o bot cria uma mão com 3 cartas e se as cartas são objetos válidos."""
    bot.criar_mao(baralho)
    assert len(bot.mao) == 3
    assert all(isinstance(carta, object) for carta in bot.mao) 

def test_enriquecer_bot(bot, dados_mock):
    """Testa se o bot pode ser enriquecido com dados."""
    bot.rodada = 1
    bot.enriquecer_bot(dados_mock, carta_baixa_ouro, carta_alta_ouro, ganhador=None)
    dados_mock.primeira_rodada.assert_called_once()

    bot.rodada = 2
    bot.enriquecer_bot(dados_mock, carta_baixa_ouro, carta_alta_ouro, ganhador=None)
    dados_mock.segunda_rodada.assert_called_once()

    bot.rodada = 3
    bot.enriquecer_bot(dados_mock, carta_baixa_ouro, carta_alta_ouro, ganhador=None)
    dados_mock.terceira_rodada.assert_called_once()

    bot.rodada = 4
    bot.enriquecer_bot(dados_mock, carta_baixa_ouro, carta_alta_ouro, ganhador=None)
    dados_mock.finalizar_rodadas.assert_called_once()

def test_enriquecer_cartas_bot(bot, cbr_mock, carta_baixa_ouro):
    """Testa se a função chama o método cbr.enriquecer_jogadas_bot."""
    bot.enriquecer_cartas_bot(cbr_mock, carta_baixa_ouro)
    cbr_mock.enriquecer_jogadas_bot.assert_called_once_with(carta_baixa_ouro)

def test_jogar_carta(bot, cbr_mock, truco_mock):
    """Testa primeiro if: self.mao com 3 cartas e flor"""
    bot.mao = [Carta(1, "OUROS"), Carta(12, "OUROS"), Carta(7, "OUROS")]
    cbr_mock.flor.return_value = True
    resultado = bot.jogar_carta(cbr_mock, truco_mock)
    assert resultado == 5

    """Testa segundo if: self.mao com 2 cartas ou menos e não pediu truco"""
    bot.mao = [Carta(1, "OUROS"), Carta(12, "ESPADAS")]
    bot.pediu_truco = False
    bot.mao_rank = [1, 2]
    bot.indices = [0, 1]
    bot.pontuacao_cartas = [10, 11]
    bot.jogar_carta(cbr_mock, truco_mock)
    cbr_mock.truco.assert_called_once_with('truco', 1, bot.qualidade_mao)

    """Testa if dentro do if: truco in [1,2]"""
    bot.mao = [Carta(1, "OUROS")]
    bot.pediu_truco = False
    cbr_mock.truco.return_value = 1
    resultado = bot.jogar_carta(cbr_mock, truco_mock)
    assert bot.pediu_truco is True
    assert resultado == 4

    """Testa parte final // não caiu em nenhum if"""

    bot.mao = [Carta(1, "OUROS"), Carta(12, "ESPADAS"), Carta(7, "OUROS")]
    cbr_mock.flor.return_value = False
    bot.rodada = 1
    bot.pontuacao_cartas = [5, 10, 15]
    cbr_mock.jogar_carta.return_value = 0
    resultado = bot.jogar_carta(cbr_mock, truco_mock)
    assert resultado == 0
    assert bot.rodada == 2

def test_calcula_envido(bot, mao):
    """Testa se o cálculo do envido está correto."""
    bot.mao = mao
    resultado = bot.calcula_envido(bot.mao)
    assert resultado == 30

    bot.mao = [Carta(1, "OUROS"), Carta(2, "ESPADAS"), Carta(3, "COPAS")]
    resultado = bot.calcula_envido(bot.mao)
    assert resultado == 3
    
    bot.mao = [Carta(11, "OUROS"), Carta(10, "ESPADAS"), Carta(3, "OUROS")]
    resultado = bot.calcula_envido(bot.mao)
    assert resultado == 3

def test_retorna_pontos_envido(bot):
    """Testa se o retorno dos pontos de envido está correto."""
    assert bot.envido == 0

def test_ajustar_indices(bot_indices, i):
    """Testa se os valores são ajustados corretamente quando faz pop()."""
    bot_indices.ajustar_indices(i)
    if i == 0:
        assert bot_indices.mao_rank == [20, 30]
        assert bot_indices.indices == [1, 2]
        assert bot_indices.pontuacao_cartas == [15, 25]
    elif i == 1:
        assert bot_indices.mao_rank == [10, 30]
        assert bot_indices.indices == [0, 2]
        assert bot_indices.pontuacao_cartas == [5, 25]
    elif i == 2:
        assert bot_indices.mao_rank == [10, 20]
        assert bot_indices.indices == [0, 1]
        assert bot_indices.pontuacao_cartas == [5, 15]

def test_mostrar_mao(bot, mao_mock):
    """Testa se mostrar_mao chama exibir_carta para cada carta na mão."""
    bot.mao = mao_mock
    bot.mostrar_mao()
    for i, carta in enumerate(mao_mock):
        carta.exibir_carta.assert_called_once_with(i)

def test_adicionar_pontos(bot, pontos=5):
    """Testa se os pontos são adicionados corretamente ao bot."""
    bot.adicionar_pontos(pontos)
    assert bot.pontos == pontos

def test_adicionar_rodada(bot):
    """Testa se a rodada é incrementada corretamente."""
    bot.adicionar_rodada()
    assert bot.rodadas == 1

def test_checa_mao(bot, mao):
    """Testa se a mão do bot é checada corretamente."""
    bot.mao = mao
    resultado = bot.checa_mao()
    assert resultado == mao

def test_checa_flor(bot, mao, mao_com_flor):
    """Testa se a verificação de flor está correta."""
    bot.mao = mao_com_flor
    resultado = bot.checa_flor()
    assert resultado == True

    bot.mao = mao
    resultado = bot.checa_flor()
    assert resultado == False

@pytest.mark.parametrize("retorno", [0, 1, 2])
def test_avaliar_truco(bot, cbr_mock, retorno):
    """Testa se o bot retorna 0, 1, 2."""
    cbr_mock.truco.return_value = retorno
    bot.qualidade_mao = 5

    resultado = bot.avaliar_truco(cbr_mock, "truco", 1)
    
    cbr_mock.truco.assert_called_once_with("truco", 1, 5)
    assert resultado == retorno


def test_avaliar_envido(bot, cbr_mock):
    """Testa se chama cbr.envido e atribui 'perdendo' corretamente."""
    bot.pontos = 7
    bot.envido = 10

    """"Testa if: pontos_totais_adversario > 6 """
    bot.avaliar_envido(cbr_mock, tipo=6, quem_pediu=1, pontos_totais_adversario=10)
    cbr_mock.envido.assert_called_once_with(6, 1, 10, True)
    cbr_mock.envido.reset_mock()

    """"Testa if: pontos_totais_adversario > pontos/1.5 """
    bot.avaliar_envido(cbr_mock, tipo=6, quem_pediu=1, pontos_totais_adversario=5)
    cbr_mock.envido.assert_called_once_with(6, 1, 10, True)
    cbr_mock.envido.reset_mock()

    """"Testa else """
    bot.avaliar_envido(cbr_mock, tipo=6, quem_pediu=1, pontos_totais_adversario=4)
    cbr_mock.envido.assert_called_once_with(6, 1, 10, False)

"""def calcular_qualidade_mao(bot, cbr_mock):
   
    bot.qualidade_mao = 5"""

def test_retorna_pontos_totais(bot, pontos):
    """Testa se o retorno dos pontos totais está correto."""
    bot.pontos = pontos
    assert bot.retorna_pontos_totais() == pontos

def test_resetar(bot_reset):
    bot_reset.resetar()
    assert bot_reset.mao == []
    assert bot_reset.mao_rank == []
    assert bot_reset.indices == []
    assert bot_reset.pontuacao_cartas == []
    assert bot_reset.qualidade_mao == 0
    assert bot_reset.rodadas == 0
    assert bot_reset.envido == 0
    assert bot_reset.rodada == 1
    assert bot_reset.flor == False
    assert bot_reset.pediu_flor == False
    assert bot_reset.pediu_truco == False