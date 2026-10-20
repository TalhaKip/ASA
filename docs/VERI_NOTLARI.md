# Veri Notları — Başlamadan Okuyun

Yarışma yönergesindeki kritik noktaların ekip içi özeti.

## 1. Dosyalar
| Dosya | Ne | Satır | Yıllar |
|---|---|---|---|
| `..._Medium_csv.gz` | Ana veri: BM'nin en iyi tahmin serisi (geçmiş + orta senaryo projeksiyonu) | ~84 bin | 1950–2101 |
| `..._OtherVariants_csv.gz` | **Opsiyonel.** Alternatif senaryolar ve olasılık aralıkları | ~663 bin | 2024–2101 |
| `..._notes.csv` | Gösterge sözlüğü (kısaltma → anlam, birim) | 54 | — |

- `.gz` dosyalarını **açmayın**; pandas doğrudan okur (`src/veri.py` doğru ayarları kullanır).
- Excel'de bakmak isterseniz: dosyayı çıkarın, uzantısı `_csv` olarak kalır, `.csv` yapın.
  Ama çıkarılmış dosyayı `data/raw/` içinde bırakmayın, kod `.gz` dosyasını bekler.

## 2. EN BÜYÜK TUZAK: Çift sayım
`Location` kolonunda sadece ülkeler yok; bölgeler, gelir grupları ve ~230+ özel topluluk da var.
Bunları ayırmadan toplarsanız nüfusu **birkaç kez** sayarsınız.

- Ülke = `ISO3_code` dolu olan satır → `src/konumlar.py: ulke_mi()`
- `LocTypeName` tutarlı etiketlenmemiş, tek başına güvenmeyin.
- Karşılaştırma ve toplamalarda **her zaman** `hazir_veri(sadece_ulke=True)` kullanın.
- `python -m src.hazirla` ülke toplamını "World" satırıyla karşılaştırır, ~%100 çıkmalı.

## 3. Tahmin mi, projeksiyon mu?
- Seri tek parça görünür ama **2023'e kadar** nüfus sayımı/anket temelli tahmin,
  **2024'ten itibaren** BM'nin orta senaryo projeksiyonudur (varsayımlara dayalı, kesin değil).
- `donem` kolonu bunu ayırır. Grafiklerde `gorsel.projeksiyon_isaretle(ax)` ile gölgeleyin.
- Raporda projeksiyon yıllarından bahsederken "BM orta senaryosuna göre" deyin.

## 4. Eksik göstergeler
Sözlükte olan ama veri dosyalarında **olmayan** göstergeler:
`LE60, LE60Male, LE60Female, BirthsMale, BirthsFemale`. Veri dosyalarında 54 gösterge kolonu var.

## 5. Birimler
Nüfus, doğum, ölüm ve göç sayıları **bin kişi** cinsindendir. Oranlar çoğunlukla **1.000 kişi başına**,
`PopGrowthRate` ise **yüzde**. Birim için: `from src.gostergeler import aciklama`.

## 6. OtherVariants (Üye 4)
- `Variant` kolonu 18 farklı değer alır: High, Low, Constant fertility, Constant mortality,
  Zero migration, Instant replacement, Momentum, ... ve Lower/Upper 80 PI, Lower/Upper 95 PI, Median PI, Mean.
- Sadece 2024–2101. Medium serisiyle birleştirirken yılları eşleyin.
- Dosya büyük: `veri.varyant_yukle(varyantlar=[...], kolonlar=[...])` ile sadece gerekeni okuyun.
