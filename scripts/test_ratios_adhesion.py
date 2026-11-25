"""Tests du recalage des ratios d'adhésion (historique de l'année)."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from app_simulation_interactive import (  # noqa: E402
    calculer_repartition_cotisations,
    normaliser_ratios_pct,
)


def test_historique_exact():
    """14 / 28 / 58 restent tels quels."""
    ratios = normaliser_ratios_pct(14, 28, 58)
    assert abs(ratios['solidaire'] - 0.14) < 1e-9
    assert abs(ratios['normale'] - 0.28) < 1e-9
    assert abs(ratios['soutien'] - 0.58) < 1e-9
    assert abs(sum(ratios.values()) - 1) < 1e-9


def test_normalise_si_total_different_de_100():
    """7 + 14 + 29 = 50, mêmes proportions que 14 / 28 / 58."""
    ratios = normaliser_ratios_pct(7, 14, 29)
    assert abs(ratios['solidaire'] - 0.14) < 1e-9
    assert abs(ratios['normale'] - 0.28) < 1e-9
    assert abs(ratios['soutien'] - 0.58) < 1e-9


def test_parts_nulles_retombe_sur_historique():
    """Trois zéros : on ne répartit pas au hasard."""
    ratios = normaliser_ratios_pct(0, 0, 0)
    assert ratios == {
        'solidaire': 0.14,
        'normale': 0.28,
        'soutien': 0.58,
    }


def test_repartition_sur_100_adherents():
    """Le mix global ignore le profil."""
    df = pd.DataFrame([{
        'age_group': '25-34',
        'csp': 'Actifs',
        'nb_adherents': 100,
    }])
    out = calculer_repartition_cotisations(
        df,
        5,
        10,
        20,
        {},
        proportions_globales=normaliser_ratios_pct(14, 28, 58),
    )
    assert int(out.loc[0, 'nb_solidaire']) == 14
    assert int(out.loc[0, 'nb_normale']) == 28
    assert int(out.loc[0, 'nb_soutien']) == 58
    # 0,14*5 + 0,28*10 + 0,58*20 = 15,1
    assert abs(out.loc[0, 'cotisation_moyenne'] - 15.1) < 1e-9


def test_repartition_sur_lignes_petites():
    """20 lignes de 4 adhérents : le total suit 14 / 28 / 58."""
    df = pd.DataFrame([
        {
            'age_group': '35-44',
            'csp': 'Actifs',
            'nb_adherents': 4,
        }
        for _ in range(20)
    ])
    out = calculer_repartition_cotisations(
        df,
        5,
        10,
        20,
        {},
        proportions_globales=normaliser_ratios_pct(14, 28, 58),
    )
    assert int(out['nb_solidaire'].sum()) == 11
    assert int(out['nb_normale'].sum()) == 23
    assert int(out['nb_soutien'].sum()) == 46
    assert int(out['nb_adherents'].sum()) == (
        int(out['nb_solidaire'].sum())
        + int(out['nb_normale'].sum())
        + int(out['nb_soutien'].sum())
    )


def test_recalage_ignore_la_regle_justificatif():
    """Le mix historique prime sur le verrou solidaire."""
    df = pd.DataFrame([{
        'age_group': '35-44',
        'csp': 'Actifs',
        'nb_adherents': 100,
    }])
    out = calculer_repartition_cotisations(
        df,
        5,
        10,
        20,
        {},
        mode_justificatif=True,
        proportions_globales=normaliser_ratios_pct(14, 28, 58),
    )
    assert int(out.loc[0, 'nb_solidaire']) == 14
    assert int(out.loc[0, 'nb_normale']) == 28
    assert int(out.loc[0, 'nb_soutien']) == 58


def test_zero_adherent_garde_tarif_normal():
    """Aucun adhérent : cotisation moyenne = tarif normal."""
    df = pd.DataFrame([{
        'age_group': '65+',
        'csp': 'Retraites',
        'nb_adherents': 0,
    }])
    out = calculer_repartition_cotisations(
        df,
        5,
        10,
        20,
        {},
        proportions_globales={
            'solidaire': 0.14,
            'normale': 0.28,
            'soutien': 0.58,
        },
    )
    assert out.loc[0, 'nb_solidaire'] == 0
    assert out.loc[0, 'nb_soutien'] == 0
    assert out.loc[0, 'cotisation_moyenne'] == 10


def main():
    """Lance les cas et renvoie 0 si tout passe."""
    tests = [
        test_historique_exact,
        test_normalise_si_total_different_de_100,
        test_parts_nulles_retombe_sur_historique,
        test_repartition_sur_100_adherents,
        test_repartition_sur_lignes_petites,
        test_recalage_ignore_la_regle_justificatif,
        test_zero_adherent_garde_tarif_normal,
    ]
    for test in tests:
        test()
        print(f"[OK] {test.__name__}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
