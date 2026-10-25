#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/isletmeler.csv dosyasindan ozet tablolarini uretir.

Kullanim:  python scripts/ozet_uret.py
Cikti:     ozet-sektor.csv, ozet-il.csv, ozet-ilce.csv, ozet-il-sektor.csv,
           ozet-yil.csv, ozet-puan-dagilimi.csv, sektorler.csv, ozet.json
"""
import csv
import io
import json
import os
import statistics
from collections import Counter, defaultdict

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERI = os.path.join(KOK, "data")
SURUM = "2026.10"
GUNCELLEME = "2026-10-25"

with io.open(os.path.join(VERI, "isletmeler.csv"), encoding="utf-8") as f:
    kayitlar = list(csv.DictReader(f))

tr = [r for r in kayitlar if r["ulke"] == "TR"]
disi = [r for r in kayitlar if r["ulke"] != "TR"]


def puan(r):
    return float(r["google_puan"]) if r["google_puan"] else None


def yorum(r):
    return int(r["google_yorum_sayisi"] or 0)


def sahne(r):
    return int(r["sahne_sayisi"] or 0)


def ortalama(satirlar):
    p = [puan(r) for r in satirlar if puan(r) is not None]
    return round(statistics.mean(p), 2) if p else ""


def yaz(ad, basliklar, satirlar):
    with io.open(os.path.join(VERI, ad), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(basliklar)
        w.writerows(satirlar)
    print("  %-26s %d satir" % (ad, len(satirlar)))


print("Ozet tablolari uretiliyor (%d kayit, %d TR)..." % (len(kayitlar), len(tr)))

# --- sektor ---
sek = defaultdict(list)
for r in tr:
    sek[(r["sektor_kod"], r["sektor"])].append(r)
satirlar = []
for (kod, ad), g in sorted(sek.items(), key=lambda x: -len(x[1])):
    y = [yorum(r) for r in g]
    satirlar.append([
        kod, ad, len(g), round(100.0 * len(g) / len(tr), 1), ortalama(g),
        statistics.median(y) if y else 0, sum(y), sum(sahne(r) for r in g),
    ])
yaz("ozet-sektor.csv",
    ["sektor_kod", "sektor", "isletme_sayisi", "pay_yuzde", "ort_google_puan",
     "medyan_yorum", "toplam_yorum", "toplam_sahne"], satirlar)

# --- sektor sozlugu (yurt disi dahil) ---
tum_sek = defaultdict(list)
for r in kayitlar:
    tum_sek[(r["sektor_kod"], r["sektor"])].append(r)
yaz("sektorler.csv", ["sektor_kod", "sektor", "isletme_sayisi"],
    [[k, a, len(g)] for (k, a), g in sorted(tum_sek.items())])

# --- il ---
il = defaultdict(list)
for r in tr:
    il[r["il"]].append(r)
satirlar = []
for ad, g in sorted(il.items(), key=lambda x: -len(x[1])):
    satirlar.append([
        ad, len(g), len(set(r["ilce"] for r in g)), ortalama(g),
        sum(yorum(r) for r in g), sum(sahne(r) for r in g),
    ])
yaz("ozet-il.csv",
    ["il", "isletme_sayisi", "ilce_sayisi", "ort_google_puan", "toplam_yorum",
     "toplam_sahne"], satirlar)

# --- ilce ---
ilce = defaultdict(list)
for r in tr:
    ilce[(r["il"], r["ilce"])].append(r)
yaz("ozet-ilce.csv", ["il", "ilce", "isletme_sayisi", "ort_google_puan"],
    [[i, c, len(g), ortalama(g)] for (i, c), g in
     sorted(ilce.items(), key=lambda x: (x[0][0], -len(x[1])))])

# --- il x sektor ---
capraz = Counter((r["il"], r["sektor_kod"], r["sektor"]) for r in tr)
yaz("ozet-il-sektor.csv", ["il", "sektor_kod", "sektor", "isletme_sayisi"],
    [[i, k, a, n] for (i, k, a), n in sorted(capraz.items(), key=lambda x: (x[0][0], -x[1]))])

# --- cekim yili ---
yil = defaultdict(list)
for r in kayitlar:
    if r["cekim_yili"]:
        yil[int(r["cekim_yili"])].append(r)
yaz("ozet-yil.csv", ["cekim_yili", "isletme_sayisi", "toplam_sahne", "il_sayisi"],
    [[y, len(g), sum(sahne(r) for r in g), len(set(r["il"] for r in g))]
     for y, g in sorted(yil.items())])

# --- puan dagilimi ---
araliklar = [("5.0", 5.0, 5.01), ("4.5-4.9", 4.5, 5.0), ("4.0-4.4", 4.0, 4.5),
             ("3.5-3.9", 3.5, 4.0), ("3.0-3.4", 3.0, 3.5), ("3.0 alti", 0.0, 3.0)]
puanli = [r for r in kayitlar if puan(r) is not None]
yaz("ozet-puan-dagilimi.csv", ["aralik", "isletme_sayisi", "pay_yuzde"],
    [[ad, n, round(100.0 * n / len(puanli), 1)] for ad, alt, ust in araliklar
     for n in [sum(1 for r in puanli if alt <= puan(r) < ust)]])

# --- ozet.json ---
tr_puanli = [r for r in tr if puan(r) is not None]
tr_yorum = [yorum(r) for r in tr]
ozet = {
    "veri_seti": "Türkiye Sanal Tur Veri Seti",
    "surum": SURUM,
    "guncelleme": GUNCELLEME,
    "kaynak": "G360 (https://g360.ai)",
    "lisans": "CC BY 4.0",
    "kapsam": {"toplam_kayit": len(kayitlar), "turkiye": len(tr), "yurtdisi": len(disi)},
    "turkiye": {
        "isletme": len(tr),
        "il": len(il),
        "ilce": len(ilce),
        "sektor": len(sek),
        "toplam_sahne": sum(sahne(r) for r in tr),
        "street_view_yayinli": sum(1 for r in tr if r["street_view_var"] == "1"),
        "ortalama_google_puan": round(statistics.mean([puan(r) for r in tr_puanli]), 2) if tr_puanli else None,
        "toplam_google_yorum": sum(tr_yorum),
        "medyan_google_yorum": statistics.median(tr_yorum) if tr_yorum else 0,
        "puan_4_5_ve_uzeri": sum(1 for r in tr_puanli if puan(r) >= 4.5),
        "en_buyuk_sektor": max(sek.items(), key=lambda x: len(x[1]))[0][1],
        "en_yogun_il": max(il.items(), key=lambda x: len(x[1]))[0],
    },
    "yurtdisi": {
        "isletme": len(disi),
        "bolge": sorted(set(r["il"] for r in disi)),
        "ulke": sorted(set(r["ulke"] for r in disi)),
    },
}
with io.open(os.path.join(VERI, "ozet.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(ozet, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("  %-26s %s" % ("ozet.json", json.dumps(ozet["kapsam"], ensure_ascii=False)))
