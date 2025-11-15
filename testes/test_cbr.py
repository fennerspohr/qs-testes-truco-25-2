import sys
import pytest
from sklearn.neighbors import NearestNeighbors

sys.path.append('../qs-testes-truco-25-2')

from truco.cbr import Cbr

@pytest.fixture
def cbr():
    return Cbr()

def test_carregar_dataset(cbr):
    """Testa se o dataset está sendo carregado corretamente"""
    df = cbr.carregar_dataset()
    assert df.index.name == "idMao"
    assert "ESPADAS" not in df.values
    assert "OURO" not in df.values
    assert "BASTOS" not in df.values
    assert "COPAS" not in df.values
    for i in df.columns.to_list():
        assert df[i].dtype == "int16"

def test_vizinhos_proximos(cbr):
    """Testa se a função retorna um objeto NearestNeighbors"""
    assert type(cbr.vizinhos_proximos(None)) == NearestNeighbors

def test_jogar_carta(cbr):
    """Testa se o método jogar_carta retorna o índice correto da carta a ser jogada"""
    # a última rodada 1 em que o bot venceu ele jogou uma carta de valor 1
    assert cbr.jogar_carta(1, [1, 2, 3]) == 0
    # a última rodada 2 em que o bot venceu ele jogou uma carta de valor 2
    assert cbr.jogar_carta(2, [7, 3, 5]) == 1
    # a última rodada 3 em que o bot venceu ele jogou uma carta de valor 7
    assert cbr.jogar_carta(3, [9, 3, 12]) == 0

def test_truco(cbr):
    """Testa se o método truco retorna a melhor opção entre aceitar, aumentar ou fugir"""
    
    #a qualidade da mão humana é 0; o bot venceu 2 e perdeu 1
    # 2 = retruco; 1 = aceitar; 0 = recusar
    assert cbr.truco(1,1,1) == 2
    assert cbr.truco(1,1,0) == 0

def test_envido(cbr, capsys):
    """Testa se o método envido retorna a melhor opção entre aceitar, pedir real envido, falta envido, ou fugir"""
    #envido_ganhas = 2, envido_perdidas = 0, real_envido_ganhas = 0, real_envido_perdidas = 0, falta_envido_ganhas = 0, falta_envido_perdidas = 0, pontos_jogador = 4

    # se bot pediu envido
        #se tem pontos > 5 e está perdendo
    assert cbr.envido(0, 2, 6, True) == 8
        # se tem pontos > 5 e está ganhando
    assert cbr.envido(0,2,6,False) == 6

    # se humano pediu envido
        # se tipo = 6
    assert cbr.envido(6,1,6, False) == 1
        # se tipo = 7
            # se robo tem mais pontos que jogador
    assert cbr.envido(7, 1, 6, True) == 1
            # se não
    assert cbr.envido(7, 1, 4, True) == 0
        # se tipo é qualquer outro numero
            # se robo tem mais pontos que jogador
    assert cbr.envido(0, 1, 6, True) == 1
            # se não
    assert cbr.envido(0, 1, 4, True) == 0
    