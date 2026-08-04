# Turkey Virtual Tour Dataset

An open dataset covering **1,202 businesses in Türkiye** whose 360° virtual tours have been
captured and published on Google Maps, with their sectoral and geographic distribution.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
![Records](https://img.shields.io/badge/records-1%2C202-green)
![Provinces](https://img.shields.io/badge/provinces-54-green)

Compiled from the archive produced by [G360](https://g360.ai) since 2018. To our knowledge
this is the only structured open dataset showing where virtual tour adoption concentrates in
Türkiye, by sector and by city.

## Headline figures

| | |
|---|---|
| Businesses (Türkiye) | **1,202** |
| Provinces | **54** |
| Districts | **183** |
| Sectors | **25** |
| Average Google rating | **4.28** |
| Total Google reviews | **792,602** |
| Rated 4.5 or above | **514** (43%) |
| Largest sector | Restaurants (369 · 30.7%) |
| Densest province | Ankara (217) |

The dataset also contains 45 records from Canada; summary tables cover Türkiye only.

## Files

| File | Contents |
|---|---|
| `data/isletmeler.csv` | All records, business level (1,247 rows) |
| `data/isletmeler.json` | Same data in JSON |
| `data/ozet-sektor.csv` | Distribution and ratings by sector |
| `data/ozet-il.csv` | Distribution by province |
| `data/ozet-ilce.csv` | Distribution by district |
| `data/ozet-il-sektor.csv` | Province × sector intersection |
| `data/ozet.json` | Machine-readable headline figures |

Column names are Turkish. Key fields: `ad` (name), `il` (province), `ilce` (district),
`sektor` (sector), `google_puan` (rating), `google_yorum_sayisi` (review count),
`enlem`/`boylam` (lat/lng), `tur_url` (virtual tour page).

## Quick start

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/g360ai/turkiye-sanal-tur-verisi/main/data/isletmeler.csv"
)
tr = df[df.ulke == "TR"]
print(tr.sektor.value_counts())
```

## Methodology and limitations

See [METODOLOJI.md](METODOLOJI.md) (Turkish). In short:

- **This is not a census of Türkiye.** It is the record of tours produced by G360 and
  published on Google Maps. It cannot be used to estimate total market size.
- **Ratings and review counts are not outcomes of the virtual tour.** They reflect each
  business's general Google performance. The dataset makes no causal claim.
- **Sector is assigned from the primary category.** For multi-category records the first
  category is used.
- **The sample is not random.** Businesses entered this archive through a commercial
  process, so both geographic and sectoral distribution are biased.

## Citation

Required under CC BY 4.0.

> G360. (2026). *Turkey Virtual Tour Dataset* (Version 2026.08) [Data set].
> https://github.com/g360ai/turkiye-sanal-tur-verisi

Machine-readable: [CITATION.cff](CITATION.cff)

## Who produced this

[G360](https://g360.ai) has produced 360° virtual tours since 2018, based in Ankara and
operating across Türkiye and Northern Cyprus. Every tour in this dataset was captured by
G360 and published on Google Maps.

Contact: bilgi@g360.ai

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
