# Ekip Çalışma Kuralları

## Altın kurallar
1. `main` her zaman çalışır durumda. Doğrudan `main`'e push yok, Pull Request ile birleştirilir.
2. Her iş için ayrı branch: `feature/isim-konu` (ör. `feature/ayse-goc-analizi`).
3. Veri dosyaları asla commit'lenmez (`.gitignore` engelliyor).
4. Herkes **kendi analiz modülünde** ve **kendi notebook'unda** çalışır.
   Ortak dosyalarda (`konumlar.py`, `gostergeler.py`, `gorsel.py`, `config.yaml`) değişiklik yapacaksanız
   gruba haber verin, küçük ve ayrı bir PR açın.
5. Grafik adları modül adıyla başlar (`belirsizlik_...png`), böylece kimse başkasının grafiğinin üstüne yazmaz.
6. Bulgularınızı `reports/bulgular/isim_konu.md` dosyasına yazın (şablon: `SABLON.md`).

## Günlük döngü

```bash
git checkout main
git pull origin main                       # 1. Güncel kodu al
git checkout -b feature/isim-konu          # 2. Branch aç

# ... çalış ...
git add src/analiz/benim_modulum.py reports/figures/ reports/bulgular/
git commit -m "Analiz: göç-büyüme saçılım grafiği"     # 3. Kaydet
git push -u origin feature/isim-konu       # 4. Gönder
```

GitHub'da **Pull Request** açın, en az bir kişi baksın, sonra birleştirin.

## Branch'i güncellemek

```bash
git checkout main && git pull origin main
git checkout feature/isim-konu
git merge main
```

## Çakışma çıkarsa

```bash
git status                 # çakışan dosyaları gör
# <<<<<<< ======= >>>>>>> kısımlarını düzelt
git add <dosya>
git commit -m "Conflict çözüldü"
# vazgeçmek için: git merge --abort
```

## Teslim öncesi sürümü işaretlemek

```bash
git tag teslim-v1 -m "Ara teslim"
git push origin --tags
```

## Commit mesajı önerisi
`Analiz: ...` · `Grafik: ...` · `Ortak: ...` (src altındaki ortak dosyalar) · `Rapor: ...` · `Düzeltme: ...`
