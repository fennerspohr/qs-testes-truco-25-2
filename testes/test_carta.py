import sys
import pytest

sys.path.append('../qs-testes-truco-25-2')
from truco.carta import Carta

def test__init__valid():
    # Testando se método __init__ de Carta cria corretamente a instância
    instance = Carta(1, "ESPADAS")
    assert instance.numero == 1
    assert instance.naipe == "ESPADAS"

