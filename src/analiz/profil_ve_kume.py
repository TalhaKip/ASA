"""ÜYE 3 — (a) Birden çok göstergeyi tek bir demografik profil ölçüsünde birleştirmek,
(b) ülkeleri tek bir yıldaki konumlarına değil, zaman içindeki hareketlerine göre gruplamak.

Seçimler (hangi göstergeler, hangi yön, eşit ağırlık mı) config.yaml'da; raporda gerekçelendirilmeli.

Kullanım: python -m src.analiz.profil_ve_kume
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from src.config import AYAR, TABLO_KLASOR
from src.gorsel import kaydet, kaynak_notu, stil_ayarla
from src.gostergeler import etiket
from src.hazirla import hazir_veri


def kompozit_indeks(ulkeler: pd.DataFrame, yil: int, gostergeler: dict[str, int]) -> pd.DataFrame:
    """Her göstergeyi z-skora çevirir, yönüyle çarpar, eşit ağırlıkla ortalar."""
    d = ulkeler[ulkeler["Time"] == yil].set_index("Location")[list(gostergeler)].dropna()
    z = (d - d.mean()) / d.std(ddof=0)
    for kod, yon in gostergeler.items():
        z[kod] *= yon
    z["indeks"] = z.mean(axis=1)
    return z.sort_values("indeks", ascending=False)


def yorunge_matrisi(ulkeler: pd.DataFrame, gostergeler: list[str], bas: int, bit: int,
                    yalnizca_degisim: bool) -> pd.DataFrame:
    """Satır = ülke, kolon = (gösterge, yıl). Her gösterge kendi içinde standartlaştırılır."""
    d = ulkeler[ulkeler["Time"].between(bas, bit)]
    bloklar = []
    for g in gostergeler:
        p = d.pivot_table(index="Location", columns="Time", values=g)
        if yalnizca_degisim:
            p = p.sub(p.iloc[:, 0], axis=0)        # her ülke kendi başlangıcına göre
        p = (p - np.nanmean(p.values)) / np.nanstd(p.values)
        p.columns = [f"{g}_{y}" for y in p.columns]
        bloklar.append(p)
    return pd.concat(bloklar, axis=1).dropna()


def yorunge_kumele(ulkeler: pd.DataFrame, ayar: dict) -> pd.Series:
    X = yorunge_matrisi(ulkeler, ayar["gostergeler"], ayar["baslangic"], ayar["bitis"],
                        ayar["yalnizca_degisim"])
    km = KMeans(n_clusters=ayar["k"], n_init=10, random_state=ayar["seed"]).fit(X.values)
    return pd.Series(km.labels_, index=X.index, name="kume")


def calistir() -> None:
    stil_ayarla()
    ulkeler = hazir_veri(sadece_ulke=True)
    TABLO_KLASOR.mkdir(parents=True, exist_ok=True)

    # (a) Bileşik indeks
    ia = AYAR["kompozit_indeks"]
    ind = kompozit_indeks(ulkeler, ia["yil"], ia["gostergeler"])
    ind.to_csv(TABLO_KLASOR / "kompozit_indeks.csv")
    uc = pd.concat([ind.head(12), ind.tail(12)])
    fig, ax = plt.subplots(figsize=(9, 8))
    renk = np.where(uc["indeks"] >= 0, "tab:green", "tab:purple")
    ax.barh(uc.index[::-1], uc["indeks"][::-1], color=renk[::-1])
    ax.axvline(0, color="grey", lw=0.8)
    ax.set(title=f"Bileşik demografik profil indeksi ({ia['yil']}) — en yüksek ve en düşük 12",
           xlabel="ortalama z-skor")
    kaynak_notu(fig, "göstergeler ve yönler: " + ", ".join(f"{k}({v:+d})" for k, v in ia["gostergeler"].items()))
    kaydet(fig, "profil_ve_kume_kompozit_indeks")

    # (b) Yörünge kümeleme
    ka = AYAR["kumeleme"]
    kume = yorunge_kumele(ulkeler, ka)
    kume.to_csv(TABLO_KLASOR / "kumeler.csv")
    print("Küme büyüklükleri:\n" + kume.value_counts().sort_index().to_string())

    d = ulkeler[ulkeler["Time"].between(ka["baslangic"], ka["bitis"])].merge(
        kume, left_on="Location", right_index=True)
    n = len(ka["gostergeler"])
    fig, axes = plt.subplots(int(np.ceil(n / 2)), 2, figsize=(14, 4 * np.ceil(n / 2)))
    for ax, g in zip(axes.flat, ka["gostergeler"]):
        ort = d.groupby(["kume", "Time"])[g].mean().unstack(0)
        for k in ort.columns:
            ax.plot(ort.index, ort[k], lw=2, label=f"Küme {k} (n={int((kume == k).sum())})")
        ax.set(title=etiket(g), xlabel="Yıl")
    for ax in list(axes.flat)[n:]:
        ax.set_visible(False)
    axes.flat[0].legend(fontsize=8)
    fig.suptitle("Ülke kümelerinin ortalama yörüngeleri", fontweight="bold")
    kaynak_notu(fig, f"{ka['baslangic']}–{ka['bitis']}, k={ka['k']}, "
                     f"{'değişime göre' if ka['yalnizca_degisim'] else 'seviyeye göre'}")
    kaydet(fig, "profil_ve_kume_yorungeler")

    # TODO (Üye 3): k seçimi (siluet skoru), indeks ağırlık duyarlılığı (sıralama ne kadar değişiyor?)


if __name__ == "__main__":
    calistir()
