# Türkiye Sanal Tur Veri Seti

Türkiye genelinde 360° sanal turu çekilip Google Haritalar'da yayınlanmış **1.202 işletmenin**
sektörel ve coğrafi dağılımını içeren açık veri seti.

[![Lisans: CC BY 4.0](https://img.shields.io/badge/Lisans-CC%20BY%204.0-blue.svg)](LICENSE)
![Kayıt](https://img.shields.io/badge/kay%C4%B1t-1.202-green)
![İl](https://img.shields.io/badge/il-54-green)
![Sürüm](https://img.shields.io/badge/s%C3%BCr%C3%BCm-2026.08-lightgrey)

Bu veri, [G360](https://g360.ai) tarafından 2018'den bu yana üretilen sanal tur arşivinden
derlenmiştir. Türkiye'de sanal tur uygulamasının hangi sektörlerde ve hangi şehirlerde
yoğunlaştığını gösteren, bilinen tek yapılandırılmış açık kaynaktır.

**Serbestçe kullanılabilir.** Tek koşul kaynak göstermek — ayrıntısı aşağıda.

---

## Özet rakamlar

| | |
|---|---|
| İşletme (Türkiye) | **1.202** |
| İl | **54** |
| İlçe | **183** |
| Sektör | **25** |
| Ortalama Google puanı | **4,28** |
| Toplam Google yorumu | **792.602** |
| 4,5 ve üzeri puanlı işletme | **514** (%43) |
| En büyük sektör | Restoran (369 · %30,7) |
| En yoğun il | Ankara (217) |

Veri setinde ayrıca yurt dışı (Kanada) 45 kayıt bulunur; özet tabloları yalnızca Türkiye
kayıtlarını kapsar.

---

## Dosyalar

| Dosya | İçerik | Satır |
|---|---|---|
| `data/isletmeler.csv` | Tüm kayıtlar, işletme düzeyinde | 1.247 |
| `data/isletmeler.json` | Aynı veri, JSON biçiminde | 1.247 |
| `data/ozet-sektor.csv` | Sektör bazında dağılım ve puan | 25 |
| `data/ozet-il.csv` | İl bazında dağılım | 54 |
| `data/ozet-ilce.csv` | İlçe bazında dağılım | 183 |
| `data/ozet-il-sektor.csv` | İl × sektör kesişimi | 290 |
| `data/ozet.json` | Üst düzey rakamlar, makine okunabilir | — |

### `isletmeler.csv` alanları

| Alan | Açıklama |
|---|---|
| `id` | Kayıt anahtarı; tur adresinde de kullanılır |
| `ad` | İşletme adı (Google İşletme Profilindeki hâliyle) |
| `ulke` | `TR` veya `CA` |
| `il` | İl |
| `ilce` | İlçe (yazım birliği sağlanmış) |
| `sektor_kod` | Makine okunabilir sektör kodu |
| `sektor` | Sektörün okunabilir adı |
| `google_puan` | Google İşletme Profili puanı (0–5) |
| `google_yorum_sayisi` | Google yorum sayısı |
| `enlem`, `boylam` | Koordinat |
| `google_cid` | Google Haritalar kalıcı işletme kimliği |
| `google_place_id` | Google Places kimliği |
| `tur_url` | İşletmenin sanal tur sayfası |

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
  kullanılmıştır.
- **Örneklem seçkisiz değildir.** İşletmeler ticari süreç sonucu bu arşive girmiştir;
  coğrafi ve sektörel dağılım bu nedenle yanlıdır.

---

## Kaynak gösterimi

Bu veriyi kullanan her çalışmada kaynak belirtilmesi gerekir (CC BY 4.0).

**Kısa biçim**

> Kaynak: G360, Türkiye Sanal Tur Veri Seti, 2026.08 — https://g360.ai/veri/sanal-tur-raporu

**Akademik biçim**

> G360. (2026). *Türkiye Sanal Tur Veri Seti* (Sürüm 2026.08) [Veri seti].
> https://github.com/g360ai/turkiye-sanal-tur-verisi

Makine okunabilir alıntı bilgisi: [CITATION.cff](CITATION.cff)

---

## Güncelleme

Veri seti sürümlenerek yayınlanır (`YYYY.AA`). Arşive yeni projeler eklendikçe yeni sürüm
çıkarılır. Canlı ve her zaman güncel özet için:
[g360.ai/veri/sanal-tur-raporu](https://g360.ai/veri/sanal-tur-raporu) ·
[JSON uç noktası](https://g360.ai/veri/sanal-tur-raporu.json)

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
