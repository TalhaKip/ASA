"""Ham WPP2024 dosyalarını okur. Okuma ayarları yarışma yönergesinden alınmıştır."""
import numpy as np
import pandas as pd

from src.config import AYAR, HAM_VERI, ISLENMIS_VERI, PROJEKSIYON_BASLANGIC

# gzip: dosyayı açmadan oku · utf-8-sig: ilk kolon adı bozulmasın · low_memory: karışık tip uyarısı çıkmasın
OKUMA_AYARI = {"compression": "gzip", "encoding": "utf-8-sig", "low_memory": False}


def _yol(anahtar: str):
    yol = HAM_VERI / AYAR["veri"][anahtar]
    if not yol.exists():
        raise FileNotFoundError(
            f"{yol.name} bulunamadı. Yarışma dosyalarını adlarını değiştirmeden "
            f"data/raw/ klasörüne koyun (README > Kurulum)."
        )
    return yol


def medium_yukle(kolonlar: list[str] | None = None) -> pd.DataFrame:
    """Ana veri (Medium). ~84 bin satır, 1950–2101."""
    return pd.read_csv(_yol("medium"), usecols=kolonlar, **OKUMA_AYARI)


def varyant_yukle(varyantlar: list[str] | None = None,
                  kolonlar: list[str] | None = None,
                  parca: int = 100_000) -> pd.DataFrame:
    """OtherVariants (opsiyonel, ~663 bin satır). Bellek dostu: parça parça okur, filtreler."""
    if kolonlar is not None and "Variant" not in kolonlar:
        kolonlar = list(kolonlar) + ["Variant"]
    parcalar = []
    for p in pd.read_csv(_yol("diger_varyantlar"), usecols=kolonlar, chunksize=parca, **OKUMA_AYARI):
        if varyantlar is not None:
            p = p[p["Variant"].isin(varyantlar)]
        parcalar.append(p)
    return pd.concat(parcalar, ignore_index=True)


def notlar_yukle() -> pd.DataFrame:
    """Gösterge sözlüğü (BM'nin orijinal açıklamaları)."""
    return pd.read_csv(_yol("notlar"), encoding="utf-8-sig")


def donem_ekle(df: pd.DataFrame) -> pd.DataFrame:
    """'tahmin' (gözleme dayalı) / 'projeksiyon' (BM orta senaryo) ayrımı."""
    df = df.copy()
    df["donem"] = np.where(df["Time"] >= PROJEKSIYON_BASLANGIC, "projeksiyon", "tahmin")
    return df


def islenmis_kaydet(df: pd.DataFrame, ad: str) -> None:
    ISLENMIS_VERI.mkdir(parents=True, exist_ok=True)
    df.to_pickle(ISLENMIS_VERI / f"{ad}.pkl")


def islenmis_yukle(ad: str) -> pd.DataFrame:
    return pd.read_pickle(ISLENMIS_VERI / f"{ad}.pkl")
