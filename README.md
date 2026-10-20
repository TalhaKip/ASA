# DataQuest 2026 — WPP2024 Demografi Analizi

4 kişilik ekibimizin ortak çalışma alanı. Veri: BM Dünya Nüfus Beklentileri 2024 (WPP2024).
**Bu repoda veri yoktur.** Herkes yarışma dosyalarını kendi bilgisayarında `data/raw/` içine koyar.

> Bu bir tahmin yarışması değil, **analiz yarışması**: çıktımız bulgular, grafikler ve rapor.

## Klasör yapısı

```
dataquest-2026/
├── config.yaml              # TÜM ayarlar (dosya adları, yıllar, örnek ülkeler, indeks seçimleri)
├── data/                    # ⛔ Git'e GİTMEZ
│   ├── raw/                 #   Yarışmanın 3 dosyası (aşağıya bakın)
│   └── processed/           #   hazırlanmış veri (otomatik oluşur)
├── src/                     # ✅ Ortak kod
│   ├── veri.py              #   Dosyaları doğru ayarlarla okur (gzip, utf-8-sig)
│   ├── konumlar.py          #   ÜLKE / BÖLGE / TOPLULUK ayrımı, bölge hiyerarşisi
│   ├── gostergeler.py       #   54 göstergenin Türkçe adı, birimi, grubu
│   ├── hazirla.py           #   Tek komutla veriyi hazırlar + kontroller
│   ├── gorsel.py            #   Ortak grafik stili, projeksiyon gölgesi, kaydetme
│   └── analiz/              #   Her üyenin analiz modülü
│       ├── yas_yapisi.py          (Üye 1)
│       ├── nufus_dinamikleri.py   (Üye 2)
│       ├── profil_ve_kume.py      (Üye 3)
│       └── belirsizlik.py         (Üye 4, OtherVariants)
├── notebooks/               # Kişisel keşif (00_baslangic.ipynb ile başlayın)
├── reports/
│   ├── figures/             # ✅ Grafikler (rapora girecek)
│   ├── tables/              # ⛔ Ara tablolar (csv, Git'e gitmez)
│   ├── bulgular/            # ✅ Her üyenin bulgu notları (SABLON.md'den kopyalayın)
│   └── final/               # ✅ Teslim edilecek rapor/sunum
├── docs/VERI_NOTLARI.md     # Veri tuzakları özeti — herkes okumalı
└── tests/                   # Veri kontrolleri (pytest)
```

## Kurulum (herkes bir kez yapar)

```bash
git clone <repo-adresi>
cd dataquest-2026
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
nbstripout --install
```

Yarışma dosyalarını **adlarını değiştirmeden ve açmadan** `data/raw/` içine koyun:

```
data/raw/WPP2024_Demographic_Indicators_Medium_csv.gz         (zorunlu)
data/raw/WPP2024_Demographic_Indicators_OtherVariants_csv.gz  (opsiyonel, Üye 4)
data/raw/WPP2024_Demographic_Indicators_notes.csv             (gösterge sözlüğü)
```

Sonra veriyi hazırlayın ve kontrol edin:

```bash
python -m src.hazirla      # okur, ülke/bölge etiketler, kontrolleri yazdırır, data/processed'e kaydeder
pytest                     # veri kontrolleri (çift sayım, gösterge sayısı vb.)
```

## Analizleri çalıştırma

```bash
python -m src.analiz.yas_yapisi
python -m src.analiz.nufus_dinamikleri
python -m src.analiz.profil_ve_kume
python -m src.analiz.belirsizlik          # OtherVariants dosyası gerekir
```

Grafikler `reports/figures/` içine, modül adıyla başlayan dosya adlarıyla kaydedilir.

## Kodda veri kullanımı

```python
from src.hazirla import hazir_veri
df = hazir_veri()                    # tüm satırlar (ülkeler + bölgeler + topluluklar)
ulkeler = hazir_veri(sadece_ulke=True)   # SADECE ülkeler -> toplama/karşılaştırma için bunu kullanın

from src.gostergeler import aciklama
aciklama("TFR")   # 'TFR: Toplam doğurganlık hızı (kadın başına canlı doğum) [Doğurganlık]'
```

`hazir_veri()` her satıra şu kolonları ekler: `ulke` (True/False), `bolge`, `alt_bolge`,
`donem` (`tahmin` = 2023'e kadar gözleme dayalı, `projeksiyon` = 2024 ve sonrası).

## Görev dağılımı (yönergedeki sorulara göre)

| Üye | Konu | Yönergedeki soru | Modül |
|---|---|---|---|
| 1 | Veri altyapısı + yaş yapısı | Yaş yapısı ülke/bölgeler arasında nasıl ayrışıyor? Tek gösterge yeter mi? | `yas_yapisi.py`, `konumlar.py` |
| 2 | Nüfus dinamikleri | Göç ile büyüme ilişkisi; doğurganlık-ölüm-göç birlikte nasıl etkiliyor? | `nufus_dinamikleri.py` |
| 3 | Profil ve kümeleme | Bileşik demografik profil ölçüsü; zaman içindeki hareketine göre ülke grupları | `profil_ve_kume.py` |
| 4 | Belirsizlik + final rapor | High/Low aralığı en geniş ülkeler; doğurganlık varsayımına duyarlılık | `belirsizlik.py`, `reports/final/` |

Git çalışma düzeni: [CONTRIBUTING.md](CONTRIBUTING.md) · Veri tuzakları: [docs/VERI_NOTLARI.md](docs/VERI_NOTLARI.md)
