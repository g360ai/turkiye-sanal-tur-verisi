# Turkey Virtual Tour Dataset

An open dataset covering **1,457 businesses in Türkiye** whose 360° virtual tours have been
captured and published on Google Maps, with their sectoral and geographic distribution.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
![Records](https://img.shields.io/badge/records-1%2C457-green)
![Provinces](https://img.shields.io/badge/provinces-55-green)
![Version](https://img.shields.io/badge/version-2026.10-lightgrey)

The data is compiled from the virtual tour archive produced by [G360](https://g360.ai)
since 2018. It is the only known structured open source showing which sectors and cities
virtual tour adoption concentrates in across Türkiye.

**Free to use.** The only condition is attribution — details below.

## Headline figures

| | |
|---|---|
| Businesses (Türkiye) | **1,457** |
| Provinces | **55** |
| Districts | **199** |
| Sectors | **25** |
| Total tour scenes | **11,618** |
| Also live on Google Street View | **1,449** |
| Average Google rating | **4.29** |
| Total Google reviews | **1,029,954** |
| Rated 4.5 or above | **607** (42%) |
| Largest sector | Restaurants (462 · 31.7%) |
| Densest province | Ankara (275) |

The dataset also contains **83** records from Canada (Alberta and Saskatchewan); summary
tables cover Türkiye only.

## Files

| File | Contents |
|---|---|
| `data/isletmeler.csv` | All records, business level (1,540 rows) |
| `data/isletmeler.json` | Same data in JSON |
| `data/isletmeler.geojson` | Same data as a point layer for GIS tools |
| `data/ozet-sektor.csv` | Distribution, ratings and scenes by sector |
| `data/ozet-il.csv` | Distribution by province |
| `data/ozet-ilce.csv` | Distribution by district |
| `data/ozet-il-sektor.csv` | Province × sector intersection |
| `data/ozet-yil.csv` | Distribution by capture year |
| `data/ozet-puan-dagilimi.csv` | Distribution by Google rating band |
| `data/sektorler.csv` | Sector code dictionary |
| `data/ozet.json` | Machine-readable headline figures |

Column names are Turkish. Key fields: `ad` (name), `il` (province), `ilce` (district),
`sektor` (sector), `google_puan` (rating), `google_yorum_sayisi` (review count),
`enlem`/`boylam` (lat/lng), `tur_url` (virtual tour page), `sahne_sayisi` (number of 360°
scenes), `street_view_var` (also published on Google Street View, `1`/`0`),
`sektor_etiketleri` (all sector tags, `|` separated), `cekim_yili` (capture year),
`yayin_yili` (publication year).

Full field reference: [VERI-SOZLUGU.md](VERI-SOZLUGU.md) (Turkish) ·
Version history: [CHANGELOG.md](CHANGELOG.md)

## Quick start

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/g360ai/turkiye-sanal-tur-verisi/main/data/isletmeler.csv"
)
tr = df[df.ulke == "TR"]
print(tr.sektor.value_counts())
print(tr.groupby("sektor").sahne_sayisi.mean().sort_values(ascending=False))
```

```python
import geopandas as gpd

gdf = gpd.read_file("data/isletmeler.geojson")
```

## Methodology and limitations

See [METODOLOJI.md](METODOLOJI.md) (Turkish). In short:

- **This is not a census of Türkiye.** It is the record of tours produced by G360 and
  published on Google Maps. It cannot be used to estimate total market size.
- **Ratings and review counts are not outcomes of the virtual tour.** They reflect each
  business's general Google performance. The dataset makes no causal claim.
- **Sector is assigned from the primary category.** For multi-category records the first
  category becomes `sektor_kod`; every tag is kept in `sektor_etiketleri`.
- **Capture year is not known for every record.** It is populated for 363 records in
  2026.10, so the year table describes that subset, not the whole archive.
- **The sample is not random.** Businesses entered this archive through a commercial
  process, so both geographic and sectoral distribution are biased.
- **No personal or contact data is published.** Phone numbers, addresses, websites,
  opening hours and review texts are deliberately excluded.

## Citation

Attribution is required for any use of this data (CC BY 4.0).

> G360. (2026). *Turkey Virtual Tour Dataset* (Version 2026.10) [Data set].
> https://github.com/g360ai/turkiye-sanal-tur-verisi

Machine-readable: [CITATION.cff](CITATION.cff)

## Who produced this

[G360](https://g360.ai) has produced 360° virtual tours since 2018, based in Ankara and
operating across Türkiye and Northern Cyprus. Every tour in this dataset was captured by
G360 and published on Google Maps.

Contact: bilgi@g360.ai

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
