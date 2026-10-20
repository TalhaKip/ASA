"""ÜYE 2 — Göç ile nüfus büyümesi arasındaki ilişki; doğurganlık, ölüm ve göç
bir ülkenin nüfus yörüngesini birlikte nasıl şekillendiriyor?

Temel özdeşlik:  PopChange ≈ NatChange (doğum − ölüm) + NetMigrations
                 PopGrowthRate (%) ≈ (NatChangeRT + CNMR) / 10

Kullanım: python -m src.analiz.nufus_dinamikleri
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import AYAR
from src.gorsel import kaydet, kaynak_notu, projeksiyon_isaretle, stil_ayarla
from src.gostergeler import etiket
from src.hazirla import hazir_veri


def bilesenler(df: pd.DataFrame, konum: str) -> pd.DataFrame:
    """Bir konumun nüfus değişiminin doğal artış ve göç bileşenleri."""
    d = df.loc[df["Location"] == konum, ["Time", "PopChange", "NatChange", "NetMigrations"]].copy()
    d["artik"] = d["PopChange"] - d["NatChange"] - d["NetMigrations"]  # ~0 olmalı
    return d


def buyume_rejimi(ulkeler: pd.DataFrame, yil: int) -> pd.DataFrame:
    """Ülkeleri doğal artış ve göç işaretine göre 4 rejime ayırır."""
    d = ulkeler[ulkeler["Time"] == yil].copy()
    dogal = np.where(d["NatChangeRT"] >= 0, "doğal artış +", "doğal artış −")
    goc = np.where(d["CNMR"] >= 0, "göç +", "göç −")
    d["rejim"] = pd.Series(dogal, index=d.index) + " / " + pd.Series(goc, index=d.index)
    return d


def calistir() -> None:
    stil_ayarla()
    df = hazir_veri()
    ulkeler = df[df["ulke"]]
    yil = AYAR["analiz"]["referans_yil"]

    # 1) Örnek ülkelerde bileşenler
    ornekler = AYAR["analiz"]["ornek_ulkeler"]
    fig, axes = plt.subplots(len(ornekler), 1, figsize=(10, 3.2 * len(ornekler)), sharex=True)
    for ax, ulke in zip(np.atleast_1d(axes), ornekler):
        b = bilesenler(df, ulke)
        if b.empty:
            ax.set_title(f"{ulke}: bulunamadı (config.yaml'daki adı kontrol edin)")
            continue
        ax.plot(b["Time"], b["NatChange"], label="Doğal artış")
        ax.plot(b["Time"], b["NetMigrations"], label="Net göç")
        ax.plot(b["Time"], b["PopChange"], color="black", lw=2, label="Toplam değişim")
        ax.axhline(0, color="grey", lw=0.8)
        projeksiyon_isaretle(ax, etiket=False)
        ax.set(title=ulke, ylabel="bin kişi")
    np.atleast_1d(axes)[0].legend(loc="upper left", ncol=3)
    fig.suptitle("Nüfus değişiminin bileşenleri", fontweight="bold")
    kaynak_notu(fig)
    kaydet(fig, "nufus_dinamikleri_bilesenler")

    # 2) Büyüme rejimleri: doğal artış hızı × net göç hızı
    d = buyume_rejimi(ulkeler, yil)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(data=d, x="NatChangeRT", y="CNMR", hue="bolge", size="TPopulation1July",
                    sizes=(15, 500), alpha=0.7, ax=ax)
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(0, color="grey", lw=0.8)
    lim = np.array(ax.get_xlim())
    ax.plot(lim, -lim, ls=":", color="black", lw=1, label="sıfır büyüme çizgisi")
    ax.set_xlim(lim)
    ax.set(title=f"Büyüme rejimleri ({yil})", xlabel=etiket("NatChangeRT"), ylabel=etiket("CNMR"))
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
    kaynak_notu(fig, "nokta boyutu = nüfus")
    kaydet(fig, "nufus_dinamikleri_buyume_rejimleri")

    print(d["rejim"].value_counts().to_string())

    # TODO (Üye 2): rejim değiştiren ülkeler (1990 vs 2023 vs 2050), bölge/gelir grubuna göre fark


if __name__ == "__main__":
    calistir()
