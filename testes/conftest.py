import sys
import pytest
sys.path.append('../qs-testes-truco-25-2')

from truco.carta import Carta
from truco.interface import Interface
from truco.jogador import Jogador
from truco.baralho import Baralho
from truco.dados import Dados
from truco.bot import Bot
from truco.cbr import Cbr
from truco.flor import Flor
from unittest.mock import MagicMock
from truco.truco import Truco

@pytest.fixture
def cbr():
    return Cbr()

@pytest.fixture
def cbr_mock():
    return MagicMock(spec=Cbr)

@pytest.fixture
def espadao():
    return Carta(1, "ESPADAS")

@pytest.fixture
def bastiao():
    return Carta(1, "BASTOS")

@pytest.fixture
def carta_alta_ouro():
    return Carta(3, "OUROS")

@pytest.fixture
def carta_baixa_ouro():
    return Carta(4, "OUROS")

@pytest.fixture
def carta_baixa_copas():
    return Carta(4, "COPAS")

@pytest.fixture
def jogador():
    return Jogador("Testes")


@pytest.fixture
def jogador2():
    return Jogador("testes 2")

@pytest.fixture
def jogadorBot2():
    return Bot("Bot")

@pytest.fixture
def jogador2_mock(pontos=0):
    return MagicMock(spec=Bot, pontos=pontos)

@pytest.fixture
def baralho():
    return Baralho()

@pytest.fixture
def dados():
    return Dados()

@pytest.fixture
def dados_mock():
    return MagicMock(spec=Dados)

@pytest.fixture
def flor():
    return Flor()

@pytest.fixture
def interface_mock():
    return MagicMock()

@pytest.fixture
def interface():
    return Interface()

@pytest.fixture
def truco():
    return Truco()
