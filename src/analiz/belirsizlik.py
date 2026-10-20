"""ÜYE 4 (OtherVariants, opsiyonel dosya)
(a) High ve Low senaryoları arasındaki fark en çok hangi ülkelerde açılıyor?
(b) Bir ülkenin 2100 projeksiyonu yalnızca doğurganlık varsayımına ne kadar duyarlı?

Kullanım: python -m src.analiz.belirsizlik
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import AYAR, TABLO_KLASOR
from src.gorsel import kaydet, kaynak_notu, stil_ayarla
from src.hazirla import hazir_veri
from src.veri import varyant_yukle

KOLONLAR = ["Location", "Variant", "Time", "TPopulation1July"]


def senaryolar_yukle() -> pd.DataFrame:
    b = AYAR["belirsizlik"]
    return varyant_yukle(varyantlar=[b["yuksek"], b["dusuk"], b["sabit_dogurganlik"]], kolonlar=KOLONLAR)


def varyant_araligi(medium_ulkeler: pd.DataFrame, varyant: pd.DataFrame, yil: int) -> pd.DataFrame:
    """Göreli aralık = (High − Low) / Medium. Büyükse ülkenin geleceği doğurganlık varsayımına çok bağlı."""
    b = AYAR["belirsizlik"]
    m = (medium_ulkeler[medium_ulkeler["Time"] == yil]
         .set_index("Location")[["bolge", "TPopulation1July"]].rename(columns={"TPopulation1July": "Medium"}))
    v = varyant[varyant["Time"] == yil].pivot_table(index="Location", columns="Variant",
                                                   values="TPopulation1July")
    t = m.join(v, how="inner")
    t["goreli_aralik"] = (t[b["yuksek"]] - t[b["dusuk"]]) / t["Medium"]
    return t.sort_values("goreli_aralik", ascending=False)


def dogurganlik_duyarliligi(medium: pd.DataFrame, varyant: pd.DataFrame, ulke: str) -> pd.DataFrame:
    """Satır = yıl, kolon = senaryo (Medium, High, Low, Constant fertility)."""
    m = medium.loc[medium["Location"] == ulke, ["Time", "TPopulation1July"]].assign(Variant="Medium")
    v = varyant.loc[varyant["Location"] == ulke, ["Time", "TPopulation1July", "Variant"]]
    return pd.concat([m, v]).pivot_table(index="Time", columns="Variant", values="TPopulation1July")


def calistir() -> None:
    stil_ayarla()
    b = AYAR["belirsizlik"]
    try:
        varyant = senaryolar_yukle()
    except FileNotFoundError as e:
        print(f"{e}\nBu analiz opsiyonel OtherVariants dosyasını gerektirir.")
        return
    medium = hazir_veri()
    ulkeler = medium[medium["ulke"]]
    varyant = varyant[varyant["Location"].isin(set(ulkeler["Location"]))]

    # (a) En belirsiz ülkeler
    t = varyant_araligi(ulkeler, varyant, b["hedef_yil"])
    TABLO_KLASOR.mkdir(parents=True, exist_ok=True)
    t.to_csv(TABLO_KLASOR / "varyant_araligi.csv")
    ilk = t[t["Medium"] >= 1000].head(20)           # 1 milyon altı küçük ülkeleri ele
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(ilk.index[::-1], ilk["goreli_aralik"][::-1] * 100)
    ax.set(title=f"{b['hedef_yil']} nüfusunda High–Low aralığı en geniş 20 ülke",
           xlabel="(High − Low) / Medium, %")
    kaynak_notu(fig, "OtherVariants · nüfusu 1 milyon altı ülkeler hariç")
    kaydet(fig, "belirsizlik_varyant_araligi")

    # (b) Örnek ülkelerde doğurganlık senaryoları
    ornekler = AYAR["analiz"]["ornek_ulkeler"]
    fig, axes = plt.subplots(int(np.ceil(len(ornekler) / 2)), 2, figsize=(14, 4.5 * np.ceil(len(ornekler) / 2)))
    stiller = {"Medium": dict(color="black", lw=2.5), b["yuksek"]: dict(ls="--"),
               b["dusuk"]: dict(ls="--"), b["sabit_dogurganlik"]: dict(ls=":", lw=2)}
    for ax, ulke in zip(axes.flat, ornekler):
        s = dogurganlik_duyarliligi(medium, varyant, ulke)
        s = s[s.index >= 1990] / 1000
        for kol in s.columns:
            ax.plot(s.index, s[kol], label=kol, **stiller.get(kol, {}))
        ax.set(title=ulke, ylabel="milyon kişi")
    for ax in list(axes.flat)[len(ornekler):]:
        ax.set_visible(False)
    axes.flat[0].legend()
    fig.suptitle("Nüfus projeksiyonu doğurganlık varsayımına ne kadar duyarlı?", fontweight="bold")
    kaynak_notu(fig, "2024 öncesi Medium tahmin serisi")
    kaydet(fig, "belirsizlik_dogurganlik_senaryolari")

    # TODO (Üye 4): Lower/Upper 95 PI ile olasılıksal aralık; bölgelere göre ortalama belirsizlik


if __name__ == "__main__":
    calistir()
