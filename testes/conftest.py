import sys
import pytest
sys.path.append('../qs-testes-truco-25-2')

from truco.carta import Carta
from truco.jogador import Jogador
from truco.baralho import Baralho

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
def baralho():
    return Baralho()