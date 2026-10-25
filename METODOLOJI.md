# Metodoloji

Bu belge, veri setinin nasıl oluşturulduğunu, hangi kararların alındığını ve sonuçların
nasıl okunması gerektiğini açıklar.

---

## 1. Evren

Veri setindeki her kayıt, **G360 tarafından 360° sanal turu çekilmiş ve Google Haritalar'da
yayınlanmış** bir işletmeye karşılık gelir.

- Toplam kayıt: **1.540**
- Türkiye: **1.457**
- Yurt dışı (Kanada — Alberta ve Saskatchewan): **83**

Özet tabloları (`ozet-*.csv`) yalnızca Türkiye kayıtlarını kapsar. `isletmeler.csv`'de her
iki grup da yer alır ve `ulke` alanıyla ayrılır.

### Bu evrenin ne olmadığı

Bu veri **Türkiye'deki tüm sanal turların sayımı değildir.** Tek bir üreticinin arşividir.
Türkiye'de başka firmalar tarafından üretilmiş, bu veri setinde yer almayan turlar vardır ve
sayıları bilinmemektedir.

Dolayısıyla bu veriden şu tür sonuçlar **çıkarılamaz:**

- "Türkiye'de X sayıda işletmenin sanal turu var"
- "Sanal tur pazarının büyüklüğü Y'dir"
- "Z sektöründe sanal tur kullanım oranı %W'dir"

Çıkarılabilecek sonuç şudur: *bu arşivde* sektörler ve şehirler nasıl dağılıyor.

---

## 2. Örneklem yanlılığı

Örneklem seçkisiz değildir. İşletmeler bu arşive ticari bir süreç sonucunda girmiştir;
yani birileri hizmet satın almıştır. Bunun üç görünür sonucu var:

**Coğrafi yanlılık.** Ankara (275) ve Muğla (128) gibi illerin öne çıkması, bu illerde sanal
turun daha yaygın olmasından değil, üreticinin saha yoğunluğundandır.

**Sektörel yanlılık.** Restoranların %31,7 pay alması, restoranların sanal tura daha yatkın
olmasını gösterebilir; ama satış odağının bu sektörde yoğunlaşmasını da gösterebilir. İki
etki bu veriyle ayrıştırılamaz.

**Zincir etkisi.** Tek bir zincir veya bayi ağıyla çalışılması, o sektörü ve o ili orantısız
biçimde büyütür. Örneğin beyaz eşya kayıtlarının 7'si tek bir ildedir.

---

## 3. Alanlar ve kaynakları

| Alan | Kaynak |
|---|---|
| `ad`, `il`, `ilce` | Google İşletme Profili |
| `sektor_kod`, `sektor` | G360 tarafından atanan birincil kategori |
| `google_puan` | Google İşletme Profili, derleme tarihindeki değer |
| `google_yorum_sayisi` | Google İşletme Profili, derleme tarihindeki değer |
| `enlem`, `boylam` | Google Places |
| `google_cid`, `google_place_id` | Google Haritalar tanımlayıcıları |
| `tur_url` | G360 tur sayfası |
| `sektor_etiketleri` | G360 kategori etiketlerinin tamamı |
| `sahne_sayisi` | G360 tur üretim kaydı |
| `street_view_var` | Turun Google Street View yayını var mı |
| `cekim_yili` | G360 saha kaydı (her kayıtta yoktur) |
| `yayin_yili` | G360 yayın kaydı (her kayıtta yoktur) |

`google_cid` kalıcıdır ve işletme taşınsa veya adını değiştirse bile değişmez;
`google_place_id` ise zaman içinde değişebilir. Eşleştirme yapacaksanız `google_cid`
tercih edilmelidir.

---

## 4. Uygulanan temizlik işlemleri

**Puan alanı tip düzeltmesi.** Kaynak veride bir bölüm kaydın puanı sayı yerine metin
olarak saklanmıştı (`"4.4"` gibi). Bu kayıtlar sayıya çevrilir. 2026.10 sürümünde
düzeltme sonrası ortalama puan **4,29**, 4,5 ve üzeri puanlı işletme sayısı **607**'dir.

**İlçe yazım birliği.** Aynı ilçe farklı büyük/küçük harf biçimleriyle kaydedilmişti
(örneğin Sivas'ta `Merkez`, `MERKEZ`, `merkez`). Her (il, ilçe) çifti için en sık kullanılan
yazım kanonik kabul edilerek diğerleri ona eşitlendi. Bu düzeltme olmadan ilçe sayısı
olduğundan yüksek çıkar; 2026.10 sürümünde yazım birliğinden sonra **199** ilçe vardır.

**Sektör ataması.** Çok kategorili kayıtlarda (`turistik,ozel` gibi) virgülden önceki ilk
kategori birincil kabul edilir ve `sektor_kod` alanına yazılır. 2026.10 ile birlikte
etiketlerin tamamı `sektor_etiketleri` alanında da korunur; 18 kayıt birden çok etiket
taşır. Bu nedenle 2026.08'de `ozel` kodunda görünen turistik mekânlar artık `turistik`
kodundadır, eski etiketleri `sektor_etiketleri` içinde durur.

**Puanı olmayan kayıtlar** ortalama hesabına dahil edilmemiştir.

---

## 5. Bilinçli olarak dışarıda bırakılanlar

**Yorum metinleri.** Kaynak arşivde işletmelere ait Google yorum metinleri bulunmaktadır.
Bunlar yorumu yazan kişilere ait içeriktir ve veri setine dahil edilmemiştir. Yalnızca
yorum *sayısı* yayınlanmaktadır.

**Telefon, adres ve web sitesi.** İşletme iletişim bilgileri Google Haritalar'da halka açık
olsa da toplu bir dosyada birleştirilmemiştir. Konum bilgisi koordinat düzeyinde
verilmektedir.

**Görseller.** Turlara ait panorama ve küçük resimler telif kapsamındadır, veri setinde yer
almaz.

**Sahne sayısı.** Kaynak arşivde bu alan bulunmakla birlikte değerleri güvenilir değildir;
yayınlanmamıştır.

---

## 6. Nedensellik uyarısı

Veri setindeki puan ve yorum sayıları, işletmelerin **genel Google performansını** yansıtır.
Bu değerler sanal turun sonucu değildir ve öyle sunulmamalıdır.

Örneğin kliniklerin ortalama puanının (4,76) arşiv ortalamasının (4,28) üzerinde olması,
"sanal tur kliniklerin puanını yükseltti" anlamına gelmez. Sağlık kuruluşlarının genel
olarak yüksek puan alması, sektörün yorum bırakma dinamiklerinin farklı olması gibi çok
sayıda açıklama mümkündür ve bu veriyle ayrıştırılamaz.

---

## 7. Sürüm ve güncelleme

Sürüm biçimi `YYYY.AA`. Bu belge **2026.10** sürümünü açıklar; derleme tarihi
**25 Ekim 2026**'dır. Sürümler arası farklar: [CHANGELOG.md](CHANGELOG.md).

Puan ve yorum sayıları derleme anındaki değerlerdir ve zaman içinde değişir. Karşılaştırmalı
analiz yapacaksanız sürüm numarasını belirtin.

Her zaman güncel özet için canlı rapora bakılabilir:
[g360.ai/veri/sanal-tur-raporu](https://g360.ai/veri/sanal-tur-raporu)

Canlı raporla bu veri seti arasında küçük farklar görülebilir; canlı rapor bazı değerleri
yuvarlar (örneğin medyan yorum sayısı canlı raporda 105, bu veri setinde tam değeriyle
104,5 verilmiştir).

---

## 8. Yeniden üretilebilirlik

`scripts/ozet_uret.py`, `data/isletmeler.csv` dosyasından tüm özet tablolarını yeniden
üretir. Böylece buradaki her sayının nasıl hesaplandığı doğrulanabilir.

```bash
python3 scripts/ozet_uret.py
```

---

## 9. Hata bildirimi

Veride hata gördüğünüzde GitHub üzerinden issue açabilir veya bilgi@g360.ai adresine
yazabilirsiniz. Düzeltmeler bir sonraki sürümde yayınlanır.
