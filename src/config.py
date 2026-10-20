"""config.yaml dosyasını okur ve proje klasör yollarını tek yerden verir."""
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[1]

with open(KOK / "config.yaml", encoding="utf-8") as f:
    AYAR = yaml.safe_load(f)

HAM_VERI = KOK / AYAR["veri"]["ham_klasor"]
ISLENMIS_VERI = KOK / AYAR["veri"]["islenmis_klasor"]
GRAFIK_KLASOR = KOK / AYAR["grafik"]["klasor"]
TABLO_KLASOR = KOK / "reports" / "tables"
PROJEKSIYON_BASLANGIC = AYAR["donem"]["projeksiyon_baslangic"]
