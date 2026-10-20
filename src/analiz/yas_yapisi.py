"""ÜYE 1 — Yaş yapısı ülkeler ve bölgeler arasında zamanla nasıl ayrışıyor?

Kullanım: python -m src.analiz.yas_yapisi
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.gorsel import kaydet, kaynak_notu, projeksiyon_isaretle, stil_ayarla
from src.gostergeler import etiket
from src.hazirla import hazir_veri
from src.konumlar import bolge_satirlari


def bolge_serisi(df: pd.DataFrame, kolon: str) -> pd.DataFrame:
    """BM'nin kendi bölge satırlarından gösterge serisi."""
    return bolge_satirlari(df)[["Location", "Time", kolon]]


def ulkeler_arasi_yayilim(ulkeler: pd.DataFrame, kolon: str) -> pd.DataFrame:
    """Her yıl ülkelerin %10, %50, %90 dilimleri. Bant genişliyorsa ülkeler ayrışıyor demektir."""
    q = ulkeler.groupby("Time")[kolon].quantile([0.1, 0.5, 0.9]).unstack()
    q.columns = ["p10", "p50", "p90"]
    q["aralik"] = q["p90"] - q["p10"]
    return q


def calistir() -> None:
    stil_ayarla()
    df = hazir_veri()
    ulkeler = df[df["ulke"]]

    # 1) Bölgelere göre medyan yaş
    t = bolge_serisi(df, "MedianAgePop")
    fig, ax = plt.subplots()
    sns.lineplot(data=t, x="Time", y="MedianAgePop", hue="Location", ax=ax)
    projeksiyon_isaretle(ax)
    ax.set(title="Bölgelere göre medyan yaş", xlabel="Yıl", ylabel=etiket("MedianAgePop"))
    ax.legend(title="")
    kaynak_notu(fig)
    kaydet(fig, "yas_yapisi_bolge_medyan_yas")

    # 2) Ülkeler arası yayılım: ayrışma artıyor mu?
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, kolon in zip(axes, ["MedianAgePop", "LE65"]):
        y = ulkeler_arasi_yayilim(ulkeler, kolon)
        ax.fill_between(y.index, y["p10"], y["p90"], alpha=0.3, label="ülkelerin %10–%90 aralığı")
        ax.plot(y.index, y["p50"], lw=2, label="medyan ülke")
        projeksiyon_isaretle(ax, etiket=False)
        ax.set(title=etiket(kolon), xlabel="Yıl")
        ax.legend(loc="upper left")
    fig.suptitle("Ülkeler arası yaş yapısı farkı zamanla nasıl değişiyor?", fontweight="bold")
    kaynak_notu(fig, "sadece ülkeler")
    kaydet(fig, "yas_yapisi_ulkeler_arasi_yayilim")

    # TODO (Üye 1): yaşlanma hızı en yüksek ülkeler (2023→2050 medyan yaş artışı),
    #               medyan yaş ile LE65 tek başına "yaş yapısını" anlatıyor mu?


if __name__ == "__main__":
    calistir()
