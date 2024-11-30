import pytest
import mastermind as m
import io

@pytest.mark.parametrize(
    "code,taille,valeurs,rs",
    [
        ([1,2,3,4],4,range(6),True),
        ([],4,range(6),False),
        ([0,1,2,3,4],4,range(6),False),
        ([6,2,3,4],4,range(6),False),
    ],
)
def test_verifier_code(code,taille,valeurs,rs):
    assert m.verifier_code(code,taille,valeurs) == rs

@pytest.mark.parametrize(
    "taille,valeurs",
    [
        (4,range(6)),
        (5,range(8)),
    ],
)
def test_generer_code(taille,valeurs):
    code = m.generer_code(taille,valeurs)
    assert m.verifier_code(code,taille,valeurs) == True

@pytest.mark.parametrize(
    "saisie,rs",
    [
        ("",[]),
        ("12",[1,2]),
    ],
)
def test_saisir_code(monkeypatch,saisie,rs):
    monkeypatch.setattr('sys.stdin', io.StringIO(saisie+"\n"))
    assert m.saisir_code() == rs

def test_erreur_saisie(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO("code\n"))
    with pytest.raises(ValueError):
        m.saisir_code()

def test_boucle_saisie(monkeypatch):
    saisie = ["","111111","test","8888","1111"]
    monkeypatch.setattr('sys.stdin',io.StringIO("\n".join(saisie)+"\n"))
    assert m.boucle_saisie(4,range(6)) == [1,1,1,1]

@pytest.fixture()
def secret():
    return [1,2,3,4]

@pytest.mark.parametrize(
    "couleur,indice,rs",
    [
        (1,0,True),
        (1,1,False),
        (5,0,False),
    ],
)
def test_est_noir(couleur,indice,secret,rs):
    assert m.est_noir(couleur,indice,secret) == rs

@pytest.mark.parametrize(
    "couleur,rs",
    [
        (1,True),
        (4,True),
        (5,False),
        (9,False),
    ],
)
def test_est_blanc(couleur,secret,rs):
    assert m.est_blanc(couleur,secret) == rs

@pytest.mark.parametrize(
    "code,nb_noir,nb_blanc",
    [
        ([5,5,5,5],0,0),
        ([1,2,3,4],4,0),
        ([4,3,2,1],0,4),
        ([1,1,1,1],1,3),
    ],
)
def test_calculer_score(code,secret,nb_noir,nb_blanc):
    score = m.calculer_score(code,secret)
    assert score['noir'] == nb_noir
    assert score['blanc'] == nb_blanc

def test_archiver(secret):
    historique = []
    code = [1,1,1,1]
    score = m.calculer_score(code, secret)
    m.archiver(historique,code,score)
    assert historique[-1] == {'code': code, 'score': score}

@pytest.mark.parametrize(
    "historique,sortie",
    [
        ([],""),
        ([{'code': [1,1,1,1], 'score': {'noir': 0, 'blanc': 0}}],
         "tour 1 - 1111 - n: 0, b: 0\n"),
        ([{'code': [1,1,1,1], 'score': {'noir': 0, 'blanc': 0}},
          {'code': [2,3,4,5], 'score': {'noir': 0, 'blanc': 2}},
          {'code': [3,2,3,2], 'score': {'noir': 1, 'blanc': 1}}],
         "tour 3 - 3232 - n: 1, b: 1\ntour 2 - 2345 - n: 0, b: 2\ntour 1 - 1111 - n: 0, b: 0\n"),
    ],
)
def test_afficher_historique(capsys,historique,sortie):
    m.afficher_historique(historique)
    capture = capsys.readouterr()
    assert capture.out == sortie

@pytest.mark.parametrize(
    "tour,score_noir,max_tours,taille,rs",
    [
        (1,0,10,4,0),
        (9,3,10,4,0),
        (1,4,10,4,1),
        (10,3,10,4,-1),
        (10,4,10,4,1),
    ],
)
def test_partie_finie(tour, score_noir, max_tours, taille, rs):
    score = {'noir': score_noir, 'blanc': 0}
    assert m.partie_finie(tour,score,max_tours,taille) == rs

def test_jouer_gagne(monkeypatch,capsys,mocker):
    mocker.patch('mastermind.generer_code', return_value=[1,2,3,4])
    saisie = ["1111","2222","1234"]
    monkeypatch.setattr('sys.stdin', io.StringIO("\n".join(saisie)+"\n"))
    m.jouer()
    capture = capsys.readouterr()
    assert "gagné" in capture.out

#@pytest.mark.skip(reason="pas encore implémenté")
def test_jouer_perdu(monkeypatch,capsys,mocker):
    mocker.patch('mastermind.generer_code', return_value=[1,2,3,4])
    saisie = ["1111","2222","3333","4444"]
    monkeypatch.setattr('sys.stdin', io.StringIO("\n".join(saisie)+"\n"))
    m.jouer(max_tours=4)
    capture = capsys.readouterr()
    assert "perdu" in capture.out

