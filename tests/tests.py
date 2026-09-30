import sys
import pandas as pd
from pathlib import Path
from pandas.testing import assert_frame_equal

# Importation du module Python à tester
module_etl = Path("../backend/etl/")
sys.path.append(str(module_etl))



def test_load_zones_csv() -> None:
    """Vérifie le nettoyage des champs, la conservation de N/A et le dédoublonnage."""
    csv_content = (
        "LocationID,Borough,Zone,service_zone\n"
        " 264 , Manhattan , N/A , Yellow Zone\n"
        "264,Duplicate,Duplicate,Duplicate\n"
        "invalid,Queens,Ignored,Green Zone\n"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = Path(temp_dir) / "zones.csv"
        csv_path.write_text(csv_content, encoding="utf-8")
        result = load_zones_csv(csv_path)

    assert len(result) == 1
    assert int(result.iloc[0]["LocationID"]) == 264
    assert result.iloc[0]["Borough"] == "Manhattan"
    assert result.iloc[0]["Zone"] == "N/A"
    assert result.iloc[0]["service_zone"] == "Yellow Zone"


def test_insert_zones(tmp_path: Path) -> None:
    """Teste l'insertion des zones, avec et sans remplacement."""
    csv_path = tmp_path / "zones.csv"
    csv_path.write_text(
        "LocationID,Borough,Zone,service_zone\n"
        "1,Manhattan,Nouvelle zone,Yellow\n"
        "2,Brooklyn,Zone Brooklyn,Boro\n",
        encoding="utf-8",
    )

    conn = sqlite3.connect(":memory:")
    try:
        conn.execute(
            "CREATE TABLE localisations "
            "(LocationID INTEGER PRIMARY KEY, Borough TEXT, Zone TEXT, service_zone TEXT)"
        )
        conn.execute(
            "INSERT INTO localisations VALUES "
            "(1, 'Manhattan', 'Zone existante', 'Yellow')"
        )

        insert_zones(conn, csv_path, replace=False)
        assert conn.execute(
            "SELECT Zone FROM localisations WHERE LocationID = 1"
        ).fetchone() == ("Zone existante",)
        assert conn.execute(
            "SELECT Zone FROM localisations WHERE LocationID = 2"
        ).fetchone() == ("Zone Brooklyn",)

        insert_zones(conn, csv_path, replace=True)
        assert conn.execute(
            "SELECT Zone FROM localisations WHERE LocationID = 1"
        ).fetchone() == ("Nouvelle zone",)
    finally:
        conn.close()