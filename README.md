# Türkiye Sanal Tur Veri Seti

Türkiye genelinde 360° sanal turu çekilip Google Haritalar'da yayınlanmış **1.457 işletmenin**
sektörel ve coğrafi dağılımını içeren açık veri seti.

[![Lisans: CC BY 4.0](https://img.shields.io/badge/Lisans-CC%20BY%204.0-blue.svg)](LICENSE)
![Kayıt](https://img.shields.io/badge/kay%C4%B1t-1.457-green)
![İl](https://img.shields.io/badge/il-55-green)
![Sürüm](https://img.shields.io/badge/s%C3%BCr%C3%BCm-2026.10-lightgrey)

Bu veri, [G360](https://g360.ai) tarafından 2018'den bu yana üretilen sanal tur arşivinden
derlenmiştir. Türkiye'de sanal tur uygulamasının hangi sektörlerde ve hangi şehirlerde
yoğunlaştığını gösteren, bilinen tek yapılandırılmış açık kaynaktır.

**Serbestçe kullanılabilir.** Tek koşul kaynak göstermek — ayrıntısı aşağıda.

---

## Özet rakamlar

| | |
|---|---|
| İşletme (Türkiye) | **1.457** |
| İl | **55** |
| İlçe | **199** |
| Sektör | **25** |
| Toplam tur sahnesi | **11.618** |
| Google Street View'da yayınlı | **1.449** |
| Ortalama Google puanı | **4,29** |
| Toplam Google yorumu | **1.029.954** |
| 4,5 ve üzeri puanlı işletme | **607** (%42) |
| En büyük sektör | Restoran (462 · %31,7) |
| En yoğun il | Ankara (275) |

Veri setinde ayrıca yurt dışı (Kanada — Alberta ve Saskatchewan) **83** kayıt bulunur;
özet tabloları yalnızca Türkiye kayıtlarını kapsar.

---

## Dosyalar

| Dosya | İçerik | Satır |
|---|---|---|
| `data/isletmeler.csv` | Tüm kayıtlar, işletme düzeyinde | 1.540 |
| `data/isletmeler.json` | Aynı veri, JSON biçiminde | 1.540 |
| `data/isletmeler.geojson` | Aynı veri, harita yazılımları için nokta katmanı | 1.538 |
| `data/ozet-sektor.csv` | Sektör bazında dağılım, puan ve sahne | 25 |
| `data/ozet-il.csv` | İl bazında dağılım | 55 |
| `data/ozet-ilce.csv` | İlçe bazında dağılım | 199 |
| `data/ozet-il-sektor.csv` | İl × sektör kesişimi | 332 |
| `data/ozet-yil.csv` | Çekim yılına göre dağılım | 5 |
| `data/ozet-puan-dagilimi.csv` | Google puanı aralıklarına göre dağılım | 6 |
| `data/sektorler.csv` | Sektör kodu sözlüğü | 25 |
| `data/ozet.json` | Üst düzey rakamlar, makine okunabilir | — |

Alanların tam tanımı: [VERI-SOZLUGU.md](VERI-SOZLUGU.md) ·
Sürüm geçmişi: [CHANGELOG.md](CHANGELOG.md)

### `isletmeler.csv` alanları

| Alan | Açıklama |
|---|---|
| `id` | Kayıt anahtarı; tur adresinde de kullanılır |
| `ad` | İşletme adı (Google İşletme Profilindeki hâliyle) |
| `ulke` | `TR` veya `CA` |
| `il` | İl (Kanada kayıtlarında eyalet) |
| `ilce` | İlçe (yazım birliği sağlanmış) |
| `sektor_kod` | Makine okunabilir birincil sektör kodu |
| `sektor` | Sektörün okunabilir adı |
| `google_puan` | Google İşletme Profili puanı (0–5) |
| `google_yorum_sayisi` | Google yorum sayısı |
| `enlem`, `boylam` | Koordinat |
| `google_cid` | Google Haritalar kalıcı işletme kimliği |
| `google_place_id` | Google Places kimliği |
| `tur_url` | İşletmenin sanal tur sayfası |
| `sektor_etiketleri` | Tüm sektör etiketleri, `\|` ile ayrık (2026.10) |
| `sahne_sayisi` | Turdaki 360° sahne sayısı (2026.10) |
| `street_view_var` | Tur Google Street View'da da yayınlı mı: `1`/`0` (2026.10) |
| `cekim_yili` | Çekim yılı, bilinen kayıtlarda (2026.10) |
| `yayin_yili` | Yayın yılı, bilinen kayıtlarda (2026.10) |

---

## Hızlı başlangıç

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/g360ai/turkiye-sanal-tur-verisi/main/data/isletmeler.csv"
)
tr = df[df.ulke == "TR"]

# Sektör dağılımı
print(tr.sektor.value_counts())

# Sektöre göre ortalama Google puanı
print(tr.groupby("sektor").google_puan.mean().sort_values(ascending=False))

# Ankara'daki restoranlar
print(tr[(tr.il == "Ankara") & (tr.sektor_kod == "restoran")].ad.tolist())

# Tur büyüklüğü: sektöre göre ortalama sahne sayısı
print(tr.groupby("sektor").sahne_sayisi.mean().sort_values(ascending=False))
```

Harita katmanı olarak (GeoJSON, QGIS · Leaflet · Mapbox · `geopandas`):

```python
import geopandas as gpd

gdf = gpd.read_file("data/isletmeler.geojson")
print(gdf[gdf.il == "Muğla"].explore())
```

---

## Metodoloji ve sınırlar

Ayrıntılı açıklama: [METODOLOJI.md](METODOLOJI.md)

Kısaca:

- **Evren, Türkiye'nin tamamı değildir.** Bu veri, G360 tarafından çekilip Google
  Haritalar'da yayınlanan turların dökümüdür. Türkiye'deki tüm sanal turların sayımı
  değildir ve sektör büyüklüğü tahmini olarak kullanılamaz.
- **Puan ve yorum sayıları sanal turun sonucu değildir.** Bunlar işletmelerin genel Google
  performansını yansıtır; veri seti hiçbir nedensellik iddiası taşımaz.
- **Sektör ataması birincil kategoriye göredir.** Çok kategorili kayıtlarda ilk kategori
  `sektor_kod` olur; etiketlerin tamamı `sektor_etiketleri` alanında durur.
- **Çekim yılı her kayıtta yoktur.** 2026.10 sürümünde 363 kayıtta doludur; yıl bazlı tablo
  bu alt kümeyi anlatır, arşivin tamamını değil.
- **Örneklem seçkisiz değildir.** İşletmeler ticari süreç sonucu bu arşive girmiştir;
  coğrafi ve sektörel dağılım bu nedenle yanlıdır.
- **Kişisel ve iletişim verisi yayınlanmaz.** Telefon, adres, web sitesi, çalışma saatleri
  ve yorum metinleri veri setinde bilerek yer almaz.

---

## Kaynak gösterimi

Bu veriyi kullanan her çalışmada kaynak belirtilmesi gerekir (CC BY 4.0).

**Kısa biçim**

> Kaynak: G360, Türkiye Sanal Tur Veri Seti, 2026.10 — https://g360.ai/veri/sanal-tur-raporu

**Akademik biçim**

> G360. (2026). *Türkiye Sanal Tur Veri Seti* (Sürüm 2026.10) [Veri seti].
> https://github.com/g360ai/turkiye-sanal-tur-verisi

Makine okunabilir alıntı bilgisi: [CITATION.cff](CITATION.cff)

---

## Güncelleme

Veri seti sürümlenerek yayınlanır (`YYYY.AA`). Arşive yeni projeler eklendikçe yeni sürüm
çıkarılır. Canlı ve her zaman güncel özet için:
[g360.ai/veri/sanal-tur-raporu](https://g360.ai/veri/sanal-tur-raporu) ·
[JSON uç noktası](https://g360.ai/veri/sanal-tur-raporu.json)

Veri dosyaları depodaki iki betikle üretilir:

```bash
python scripts/veri_uret.py <ham-kayit.json>   # yayin dosyalarini uretir
python scripts/ozet_uret.py                    # ozet tablolarini uretir
```

---

## Veriyi kim üretti

[G360](https://g360.ai), 2018'den bu yana 360° sanal tur üretimi yapan bir görüntüleme
firmasıdır. Merkezi Ankara'dadır; Türkiye ve KKTC genelinde çalışır. Bu veri setindeki tüm
turlar G360 tarafından çekilip Google Haritalar'da yayınlanmıştır.

Sanal tur konusundaki teknik ve sektörel rehberler:
[g360.ai/rehber](https://g360.ai/rehber)

İletişim: bilgi@g360.ai

---

## Lisans

[Creative Commons Atıf 4.0 Uluslararası (CC BY 4.0)](LICENSE)

Ticari kullanım dahil serbestçe kopyalayabilir, dağıtabilir, işleyebilir ve
türev çalışma üretebilirsiniz. Tek koşul uygun şekilde kaynak göstermektir.

---

*English version: [README.en.md](README.en.md)*
