# Sürüm geçmişi

Sürüm biçimi `YYYY.AA`. Puan ve yorum sayıları derleme anındaki değerlerdir;
karşılaştırmalı analizde sürüm numarasını belirtin.

## 2026.10 — 25 Ekim 2026

**Kapsam büyüdü**

- Kayıt sayısı 1.247 → **1.540** (Türkiye 1.202 → **1.457**, Kanada 45 → **83**).
- İl 54 → **55**, ilçe 183 → **199**.
- Toplam Google yorumu 792.602 → **1.029.954**; ortalama puan 4,28 → **4,29**.

**Yeni alanlar** (`isletmeler.csv` / `.json` / `.geojson`)

| Alan | İçerik |
|---|---|
| `sektor_etiketleri` | Kaydın tüm sektör etiketleri; ilki `sektor_kod` ile aynıdır |
| `sahne_sayisi` | Turdaki 360° sahne sayısı — turun büyüklüğü |
| `street_view_var` | Tur Google Street View'da da yayınlı mı |
| `cekim_yili` | Çekim yılı (363 kayıtta dolu) |
| `yayin_yili` | Yayın yılı (1.479 kayıtta dolu) |

Eski 14 alan adı ve sırası korunmuştur; yeni alanlar sona eklenmiştir.
2026.08 için yazılmış kod değişiklik gerektirmez.

**Yeni dosyalar**

- `data/isletmeler.geojson` — harita yazılımları için nokta katmanı (1.538 nokta).
- `data/ozet-yil.csv` — çekim yılına göre dağılım.
- `data/ozet-puan-dagilimi.csv` — Google puanı aralıklarına göre dağılım.
- `data/sektorler.csv` — sektör kodu sözlüğü.
- `VERI-SOZLUGU.md` — alanların tam tanımı, doluluk oranlarıyla.
- `CHANGELOG.md` — bu dosya.
- `scripts/veri_uret.py` — yayın dosyalarını ham kayıttan üreten betik.

**Değişen tablolar**

- `ozet-sektor.csv` ve `ozet-il.csv` tablolarına `toplam_sahne` sütunu eklendi.
- `ozet-ilce.csv` tablosuna `ort_google_puan` sütunu eklendi.
- `ozet.json` içine `toplam_sahne`, `street_view_yayinli` ve `yurtdisi` bloğu eklendi.

**Sektör kodu değişikliği**

Turistik mekânlar 2026.08'de `ozel` kodundaydı; artık **`turistik`** kodundadır.
Eski etiketleri `sektor_etiketleri` alanında korunur. `ozel` kodu birincil sektör
olarak artık kullanılmaz.

**Gizlilik**

Telefon, adres, web sitesi, çalışma saatleri ve Google yorum metinleri bu veri setinde
hiçbir sürümde yer almadı. 2026.10 ile birlikte `scripts/veri_uret.py` bu alanların
çıktıya sızmadığını her çalıştırmada denetler.

## 2026.08 — 3 Ağustos 2026

İlk yayın. 1.247 kayıt (Türkiye 1.202, Kanada 45), 14 alan, 4 özet tablosu.
