"""Ülke / bölge / topluluk ayrımı.

YÖNERGEDEKİ UYARI: Location kolonu ülkelerin yanında bölgeleri, gelir gruplarını ve ~230+ özel
topluluğu da içerir. Bunları ayırmadan toplarsanız nüfusu birden çok kez sayarsınız.
Ülke = ISO3_code dolu satır. LocTypeName tutarlı değildir, tek başına güvenmeyin.
"""
import pandas as pd

DUNYA_LOCID = 900


def ulke_mi(df: pd.DataFrame) -> pd.Series:
    iso = df["ISO3_code"]
    return iso.notna() & (iso.astype(str).str.strip() != "")


def sadece_ulkeler(df: pd.DataFrame) -> pd.DataFrame:
    return df[ulke_mi(df)].copy()


def konum_ozeti(df: pd.DataFrame) -> pd.DataFrame:
    """Her LocTypeName'de kaç konum var ve kaçının ISO3 kodu var? (tutarsızlıkları görmek için)"""
    k = df.drop_duplicates("Location")
    return (
        k.assign(iso3_var=ulke_mi(k))
        .groupby("LocTypeName", dropna=False)
        .agg(konum_sayisi=("Location", "size"), iso3_olan=("iso3_var", "sum"))
        .sort_values("konum_sayisi", ascending=False)
    )


def bolge_ekle(df: pd.DataFrame) -> pd.DataFrame:
    """ParentID hiyerarşisini izleyerek her satıra 'alt_bolge' (bir üst) ve 'bolge'
    (Dünya'nın hemen altındaki kıta düzeyi) ekler."""
    if not {"LocID", "ParentID"}.issubset(df.columns):
        print("Uyarı: LocID/ParentID kolonu yok, bölge eklenemedi.")
        return df
    k = df.drop_duplicates("LocID").set_index("LocID")
    ebeveyn = k["ParentID"].to_dict()
    ad = k["Location"].to_dict()

    def atalar(locid):
        zincir, g = [], ebeveyn.get(locid)
        while g is not None and not pd.isna(g) and g in ad and g != DUNYA_LOCID and len(zincir) < 10:
            zincir.append(g)
            g = ebeveyn.get(g)
        return zincir

    alt, ust = {}, {}
    for locid in k.index:
        z = atalar(locid)
        alt[locid] = ad[z[0]] if z else None
        ust[locid] = ad[z[-1]] if z else None
    df = df.copy()
    df["alt_bolge"] = df["LocID"].map(alt)
    df["bolge"] = df["LocID"].map(ust)
    return df


def bolge_satirlari(df: pd.DataFrame) -> pd.DataFrame:
    """BM'nin kendi hesapladığı kıta düzeyi satırlar (ör. Africa, Europe).
    Bölge karşılaştırmasında ülke ortalaması yerine bunları kullanmak daha doğrudur
    (ör. bölgenin medyan yaşı, ülke medyanlarının ortalaması değildir)."""
    bolgeler = set(df.loc[ulke_mi(df), "bolge"].dropna())
    return df[df["Location"].isin(bolgeler) & ~ulke_mi(df)].copy()


def agirlikli_ortalama(df: pd.DataFrame, kolon: str, grup: list[str],
                       agirlik: str = "TPopulation1July") -> pd.DataFrame:
    """Kendi gruplamanız için nüfus ağırlıklı ortalama. Not: medyan yaş gibi göstergelerde
    bu bir yaklaşıklıktır; mümkünse BM'nin bölge satırlarını kullanın."""
    d = df.dropna(subset=[kolon, agirlik])
    t = d.assign(_c=d[kolon] * d[agirlik]).groupby(grup)[["_c", agirlik]].sum()
    return (t["_c"] / t[agirlik]).rename(kolon).reset_index()


def cift_sayim_kontrol(df: pd.DataFrame, yil: int) -> float:
    """Ülke toplamı / Dünya satırı. ~1.00 olmalı. Tüm satırların toplamı ise çok daha büyük çıkar."""
    d = df[df["Time"] == yil]
    ulke_toplam = d.loc[ulke_mi(d), "TPopulation1July"].sum()
    dunya = d.loc[d["Location"] == "World", "TPopulation1July"]
    hepsi = d["TPopulation1July"].sum()
    if dunya.empty:
        print("Uyarı: 'World' satırı bulunamadı.")
        return float("nan")
    oran = ulke_toplam / dunya.iloc[0]
    print(f"  {yil} — ülkeler toplamı / Dünya = {oran:.4f}   "
          f"(tüm satırlar toplanırsa {hepsi / dunya.iloc[0]:.1f} kat: çift sayım!)")
    return float(oran)
