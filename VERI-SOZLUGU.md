# Veri Sözlüğü

`data/isletmeler.csv`, `data/isletmeler.json` ve `data/isletmeler.geojson` dosyalarındaki
alanların tanımı. Üç dosya aynı kayıtları taşır; GeoJSON'da `enlem`/`boylam` alanları
`geometry` içinde durur, kalan alanlar `properties` altındadır.

Sürüm **2026.10** · **1540** kayıt (Türkiye 1457, Kanada 83)

## Alanlar

| Alan | Tip | Dolu | Açıklama | Örnek |
|---|---|---|---|---|
| `id` | metin | 1540 / 1540 | Kayıt anahtarı. `il_ilce_ad` biçiminde üretilmiş yazı-anahtarı; tur adresinde de geçer. | `bolu_mengen_the_uzar_coffee` |
| `ad` | metin | 1540 / 1540 | İşletme adı, Google İşletme Profilindeki hâliyle. | `The Uzar Coffee` |
| `ulke` | metin | 1540 / 1540 | `TR` veya `CA`. Özet tabloları yalnızca `TR` kayıtlarını sayar. | `TR` |
| `il` | metin | 1540 / 1540 | İl. Kanada kayıtlarında eyalet adı (`Alberta`, `Saskatchewan`). | `Bolu` |
| `ilce` | metin | 1540 / 1540 | İlçe. Yazım birliği uygulanmıştır (bkz. METODOLOJI.md, bölüm 4). | `Mengen` |
| `sektor_kod` | metin | 1540 / 1540 | Birincil sektör kodu. Tam liste: `data/sektorler.csv`. | `kafe` |
| `sektor` | metin | 1540 / 1540 | Sektör kodunun okunabilir adı. | `Kafe` |
| `google_puan` | ondalık | 1488 / 1540 | Google İşletme Profili puanı, 0–5. Derleme anındaki değerdir. | `4.6` |
| `google_yorum_sayisi` | tam sayı | 1539 / 1540 | Google yorum sayısı. Derleme anındaki değerdir. | `68` |
| `enlem` | ondalık | 1538 / 1540 | WGS84 enlem. | `40.9571467` |
| `boylam` | ondalık | 1538 / 1540 | WGS84 boylam. | `32.0850739` |
| `google_cid` | metin | 1537 / 1540 | Google Haritalar kalıcı işletme kimliği. Eşleştirmede bunu tercih edin. | `503946768474070321` |
| `google_place_id` | metin | 1536 / 1540 | Google Places kimliği. Zaman içinde değişebilir. | `ChIJ...` |
| `tur_url` | metin | 1540 / 1540 | İşletmenin sanal tur sayfası. | `https://g360.ai/vr/&lt;id&gt;` |
| `sektor_etiketleri` | metin listesi | 1540 / 1540 | Tüm sektör etiketleri. CSV'de `\|` ile ayrık, JSON'da dizi. İlki `sektor_kod` ile aynıdır. | `turistik\|ozel` |
| `sahne_sayisi` | tam sayı | 1539 / 1540 | Turdaki 360° sahne sayısı. Turun büyüklüğünü gösterir. | `6` |
| `street_view_var` | 0/1 | 1540 / 1540 | Tur Google Street View'da da yayınlı mı. CSV'de `1`/`0`, JSON'da `true`/`false`. 1.449 kayıtta `1`. | `1` |
| `cekim_yili` | tam sayı | 363 / 1540 | Çekim yılı. Yalnızca saha kaydı bulunan kayıtlarda doludur. | `2024` |
| `yayin_yili` | tam sayı | 1479 / 1540 | Yayın yılı. Yalnızca yayın kaydı bulunan kayıtlarda doludur. | `2026` |

**Boş değerler.** CSV'de boş hücre, JSON'da `null`. Puanı olmayan kayıtlar ortalama
hesaplarına katılmaz.

**Kodlama.** Tüm dosyalar UTF-8'dir; CSV ayracı virgül, satır sonu `
`.

## Özet tabloları

| Dosya | Anahtar | Kapsam |
|---|---|---|
| `ozet-sektor.csv` | `sektor_kod` | Yalnızca Türkiye |
| `ozet-il.csv` | `il` | Yalnızca Türkiye |
| `ozet-ilce.csv` | `il` + `ilce` | Yalnızca Türkiye |
| `ozet-il-sektor.csv` | `il` + `sektor_kod` | Yalnızca Türkiye |
| `ozet-yil.csv` | `cekim_yili` | Tüm kayıtlar (çekim yılı bilinenler) |
| `ozet-puan-dagilimi.csv` | `aralik` | Tüm kayıtlar (puanı olanlar) |
| `sektorler.csv` | `sektor_kod` | Tüm kayıtlar |
| `ozet.json` | — | Üst düzey rakamlar |

## Yayınlanmayan alanlar

G360'in üretim kaydında bulunan ama bu veri setine **bilerek alınmayan** alanlar:
telefon, adres, web sitesi, çalışma saatleri, Google yorum metinleri, fotoğraflar,
tur şifresi ve iç önceliklendirme alanları. `scripts/veri_uret.py` bu alanların çıktıya
sızmadığını her çalıştırmada denetler.

## Üretim

```bash
python scripts/veri_uret.py <ham-kayit.json>   # yayin dosyalarini uretir
python scripts/ozet_uret.py                    # ozet tablolarini uretir
```

Ham kayıt dosyası G360'in kendi üretim veritabanıdır ve yayınlanmaz.
