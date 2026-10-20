"""Veriyi tek komutla hazırlar, kontrolleri yazdırır, data/processed'e kaydeder.

Kullanım:
    python -m src.hazirla
Kodda:
    from src.hazirla import hazir_veri
    df = hazir_veri(sadece_ulke=True)
"""
import pandas as pd

from src.config import AYAR
from src.gostergeler import eksik_gostergeler
from src.konumlar import bolge_ekle, cift_sayim_kontrol, konum_ozeti, ulke_mi
from src.veri import donem_ekle, islenmis_kaydet, islenmis_yukle, medium_yukle

DOSYA_ADI = "medium_hazir"


def hazirla(kaydet: bool = True) -> pd.DataFrame:
    print("Medium dosyası okunuyor...")
    df = medium_yukle()
    df = donem_ekle(df)
    df["ulke"] = ulke_mi(df)
    df = bolge_ekle(df)

    print(f"\nBoyut: {df.shape[0]:,} satır × {df.shape[1]} kolon | "
          f"Yıllar: {df['Time'].min()}–{df['Time'].max()} | Variant: {df['Variant'].unique().tolist()}")
    print(f"Konum: {df['Location'].nunique()} toplam, {df.loc[df['ulke'], 'Location'].nunique()} ülke")

    print("\nKonum türleri (LocTypeName):")
    print(konum_ozeti(df).to_string())

    print("\nÇift sayım kontrolü:")
    cift_sayim_kontrol(df, AYAR["analiz"]["referans_yil"])

    eksik, fazla = eksik_gostergeler(df)
    print(f"\nGöstergeler: {54 - len(eksik)}/54 mevcut"
          + (f" | eksik: {eksik}" if eksik else "") + (f" | listede olmayan: {fazla}" if fazla else ""))

    ulke_bolgesiz = df.loc[df["ulke"] & df["bolge"].isna(), "Location"].unique() if "bolge" in df else []
    if len(ulke_bolgesiz):
        print(f"Uyarı: bölgesi bulunamayan ülkeler: {list(ulke_bolgesiz)[:10]}")

    if kaydet:
        islenmis_kaydet(df, DOSYA_ADI)
        print(f"\nKaydedildi: data/processed/{DOSYA_ADI}.pkl")
    return df


def hazir_veri(sadece_ulke: bool = False) -> pd.DataFrame:
    """Hazırlanmış veriyi döner; yoksa önce hazırlar."""
    try:
        df = islenmis_yukle(DOSYA_ADI)
    except FileNotFoundError:
        df = hazirla()
    return df[df["ulke"]].copy() if sadece_ulke else df


if __name__ == "__main__":
    hazirla()
