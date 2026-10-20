"""Veri kontrolleri. Çalıştırma: pytest
Veri dosyası yoksa testler atlanır (CI'da hata vermez)."""
import pytest

from src.config import AYAR, HAM_VERI

pytestmark = pytest.mark.skipif(
    not (HAM_VERI / AYAR["veri"]["medium"]).exists(), reason="Medium dosyası data/raw/ içinde yok"
)


@pytest.fixture(scope="module")
def df():
    from src.hazirla import hazir_veri
    return hazir_veri()


def test_konum_yil_tekil(df):
    assert not df.duplicated(["LocID", "Time"]).any()


def test_ulke_toplami_dunyaya_esit(df):
    from src.konumlar import cift_sayim_kontrol
    oran = cift_sayim_kontrol(df, AYAR["analiz"]["referans_yil"])
    assert 0.98 < oran < 1.02


def test_54_gosterge(df):
    from src.gostergeler import eksik_gostergeler
    eksik, _ = eksik_gostergeler(df)
    assert eksik == []


def test_medium_tek_variant(df):
    assert set(df["Variant"].unique()) == {"Medium"}


def test_ulkelerin_bolgesi_var(df):
    assert df.loc[df["ulke"], "bolge"].notna().mean() > 0.95


def test_donem(df):
    assert set(df["donem"]) == {"tahmin", "projeksiyon"}
