"""Veri dosyalarındaki 54 göstergenin Türkçe adı, birimi ve grubu.

Kaynak: yarışma yönergesi + notes.csv. BM'nin birebir İngilizce açıklaması için: veri.notlar_yukle()
NOT: LE60, LE60Male, LE60Female, BirthsMale, BirthsFemale sözlükte var ama veri dosyalarında YOK.
"""
import pandas as pd

# kod: (grup, Türkçe ad, birim)
GOSTERGELER = {
    "TPopulation1Jan": ("Nüfus", "Toplam nüfus (1 Ocak)", "bin kişi"),
    "TPopulation1July": ("Nüfus", "Toplam nüfus (1 Temmuz)", "bin kişi"),
    "TPopulationMale1July": ("Nüfus", "Erkek nüfus (1 Temmuz)", "bin kişi"),
    "TPopulationFemale1July": ("Nüfus", "Kadın nüfus (1 Temmuz)", "bin kişi"),
    "PopDensity": ("Nüfus", "Nüfus yoğunluğu", "kişi/km²"),
    "PopSexRatio": ("Nüfus", "Cinsiyet oranı", "100 kadına erkek"),
    "MedianAgePop": ("Nüfus", "Medyan yaş", "yıl"),
    "NatChange": ("Nüfus", "Doğal artış (doğum − ölüm)", "bin kişi"),
    "NatChangeRT": ("Nüfus", "Doğal artış hızı", "1.000 kişi başına"),
    "PopChange": ("Nüfus", "Nüfus değişimi", "bin kişi"),
    "PopGrowthRate": ("Nüfus", "Nüfus artış hızı", "yüzde"),
    "DoublingTime": ("Nüfus", "Nüfusun ikiye katlanma süresi", "yıl"),
    "Births": ("Doğurganlık", "Doğum sayısı", "bin"),
    "Births1519": ("Doğurganlık", "15-19 yaş kadınlardan doğum", "bin"),
    "CBR": ("Doğurganlık", "Kaba doğum hızı", "1.000 kişi başına doğum"),
    "TFR": ("Doğurganlık", "Toplam doğurganlık hızı", "kadın başına canlı doğum"),
    "NRR": ("Doğurganlık", "Net yeniden üretim hızı", "kadın başına hayatta kalan kız"),
    "MAC": ("Doğurganlık", "Ortalama doğurma yaşı", "yıl"),
    "SRB": ("Doğurganlık", "Doğumda cinsiyet oranı", "100 kız doğumuna erkek"),
    "Deaths": ("Ölümlülük", "Ölüm sayısı", "bin"),
    "DeathsMale": ("Ölümlülük", "Ölüm sayısı (erkek)", "bin"),
    "DeathsFemale": ("Ölümlülük", "Ölüm sayısı (kadın)", "bin"),
    "CDR": ("Ölümlülük", "Kaba ölüm hızı", "1.000 kişi başına ölüm"),
    "LEx": ("Ölümlülük", "Doğumda yaşam beklentisi", "yıl"),
    "LExMale": ("Ölümlülük", "Doğumda yaşam beklentisi (erkek)", "yıl"),
    "LExFemale": ("Ölümlülük", "Doğumda yaşam beklentisi (kadın)", "yıl"),
    "LE15": ("Ölümlülük", "15 yaşında yaşam beklentisi", "yıl"),
    "LE15Male": ("Ölümlülük", "15 yaşında yaşam beklentisi (erkek)", "yıl"),
    "LE15Female": ("Ölümlülük", "15 yaşında yaşam beklentisi (kadın)", "yıl"),
    "LE65": ("Ölümlülük", "65 yaşında yaşam beklentisi", "yıl"),
    "LE65Male": ("Ölümlülük", "65 yaşında yaşam beklentisi (erkek)", "yıl"),
    "LE65Female": ("Ölümlülük", "65 yaşında yaşam beklentisi (kadın)", "yıl"),
    "LE80": ("Ölümlülük", "80 yaşında yaşam beklentisi", "yıl"),
    "LE80Male": ("Ölümlülük", "80 yaşında yaşam beklentisi (erkek)", "yıl"),
    "LE80Female": ("Ölümlülük", "80 yaşında yaşam beklentisi (kadın)", "yıl"),
    "InfantDeaths": ("Ölümlülük", "Bebek ölümleri (1 yaş altı)", "bin"),
    "IMR": ("Ölümlülük", "Bebek ölüm hızı", "1.000 canlı doğumda"),
    "LBsurvivingAge1": ("Ölümlülük", "1 yaşına ulaşan canlı doğumlar", "bin"),
    "Under5Deaths": ("Ölümlülük", "5 yaş altı ölümler", "bin"),
    "Q5": ("Ölümlülük", "5 yaş altı ölüm hızı", "1.000 canlı doğumda"),
    "Q0040": ("Ölümlülük", "40 yaşından önce ölüm olasılığı", "1.000 canlı doğumda"),
    "Q0040Male": ("Ölümlülük", "40 yaşından önce ölüm olasılığı (erkek)", "1.000 canlı doğumda"),
    "Q0040Female": ("Ölümlülük", "40 yaşından önce ölüm olasılığı (kadın)", "1.000 canlı doğumda"),
    "Q0060": ("Ölümlülük", "60 yaşından önce ölüm olasılığı", "1.000 canlı doğumda"),
    "Q0060Male": ("Ölümlülük", "60 yaşından önce ölüm olasılığı (erkek)", "1.000 canlı doğumda"),
    "Q0060Female": ("Ölümlülük", "60 yaşından önce ölüm olasılığı (kadın)", "1.000 canlı doğumda"),
    "Q1550": ("Ölümlülük", "15-50 yaş arası ölüm olasılığı", "15 yaşında hayatta olan 1.000 kişide"),
    "Q1550Male": ("Ölümlülük", "15-50 yaş arası ölüm olasılığı (erkek)", "15 yaşında hayatta olan 1.000 kişide"),
    "Q1550Female": ("Ölümlülük", "15-50 yaş arası ölüm olasılığı (kadın)", "15 yaşında hayatta olan 1.000 kişide"),
    "Q1560": ("Ölümlülük", "15-60 yaş arası ölüm olasılığı", "15 yaşında hayatta olan 1.000 kişide"),
    "Q1560Male": ("Ölümlülük", "15-60 yaş arası ölüm olasılığı (erkek)", "15 yaşında hayatta olan 1.000 kişide"),
    "Q1560Female": ("Ölümlülük", "15-60 yaş arası ölüm olasılığı (kadın)", "15 yaşında hayatta olan 1.000 kişide"),
    "NetMigrations": ("Göç", "Net göçmen sayısı", "bin kişi"),
    "CNMR": ("Göç", "Net göç hızı", "1.000 kişi başına"),
}

KIMLIK_KOLONLARI = ["SortOrder", "LocID", "Notes", "ISO3_code", "ISO2_code", "SDMX_code",
                    "LocTypeID", "LocTypeName", "ParentID", "Location", "VarID", "Variant", "Time",
                    "ulke", "bolge", "alt_bolge", "donem"]  # son 4: hazirla.py ekler
VERIDE_OLMAYANLAR = ["LE60", "LE60Male", "LE60Female", "BirthsMale", "BirthsFemale"]


def aciklama(kod: str) -> str:
    if kod not in GOSTERGELER:
        ek = " (bu gösterge veri dosyalarında yok)" if kod in VERIDE_OLMAYANLAR else ""
        return f"{kod}: bilinmiyor{ek}"
    grup, ad, birim = GOSTERGELER[kod]
    return f"{kod}: {ad} ({birim}) [{grup}]"


def etiket(kod: str) -> str:
    """Grafik ekseni için: 'Toplam doğurganlık hızı (kadın başına canlı doğum)'"""
    if kod not in GOSTERGELER:
        return kod
    _, ad, birim = GOSTERGELER[kod]
    return f"{ad} ({birim})"


def grup_gostergeleri(grup: str) -> list[str]:
    """grup: 'Nüfus' | 'Doğurganlık' | 'Ölümlülük' | 'Göç'"""
    return [k for k, (g, _, _) in GOSTERGELER.items() if g == grup]


def gosterge_tablosu() -> pd.DataFrame:
    return pd.DataFrame(
        [(k, g, a, b) for k, (g, a, b) in GOSTERGELER.items()],
        columns=["kod", "grup", "ad", "birim"],
    )


def eksik_gostergeler(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """(beklenip veride olmayanlar, veride olup listede olmayanlar)"""
    eksik = [k for k in GOSTERGELER if k not in df.columns]
    fazla = [c for c in df.columns if c not in GOSTERGELER and c not in KIMLIK_KOLONLARI]
    return eksik, fazla
