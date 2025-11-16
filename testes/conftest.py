import sys
import pytest
sys.path.append('../qs-testes-truco-25-2')

from truco.carta import Carta
from truco.jogador import Jogador
from truco.baralho import Baralho
<<<<<<< HEAD
from truco.dados import Dados
from truco.bot import Bot
from truco.cbr import Cbr

@pytest.fixture
def cbr():
    return Cbr()
=======
from truco.flor import Flor
from unittest.mock import MagicMock
>>>>>>> 2fd8793 ([Testes] test_flor.py)

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
def jogador2():
    return Bot("Bot")

@pytest.fixture
def baralho():
    return Baralho()

@pytest.fixture
<<<<<<< HEAD
def dados():
    return Dados()
=======
def flor():
    return Flor()

@pytest.fixture
def interface_mock():
    return MagicMock()
>>>>>>> 2fd8793 ([Testes] test_flor.py)
