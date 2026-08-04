# -*- coding: utf-8 -*-
"""isletmeler.csv dosyasindan tum ozet tablolarini yeniden uretir.

Kullanim:
    python3 scripts/ozet_uret.py

Bagimlilik yok; yalnizca standart kutuphane kullanir.
"""
import csv, json, os, statistics
from collections import Counter, defaultdict

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERI = os.path.join(KOK, "data")

with open(os.path.join(VERI, "isletmeler.csv"), encoding="utf-8") as f:
    kayitlar = list(csv.DictReader(f))

tr = [r for r in kayitlar if r["ulke"] == "TR"]


def puan(r):
    return float(r["google_puan"]) if r["google_puan"] else None


def yorum(r):
    return int(r["google_yorum_sayisi"] or 0)


def yaz(ad, basliklar, satirlar):
    with open(os.path.join(VERI, ad), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(basliklar)
        w.writerows(satirlar)
    print(f"  {ad}: {len(satirlar)} satir")


print(f"Turkiye kaydi: {len(tr)} / toplam {len(kayitlar)}")

# ── sektor ─────────────────────────────────────────────────────────────
sek = defaultdict(list)
for r in tr:
    sek[r["sektor_kod"]].append(r)
yaz("ozet-sektor.csv",
    ["sektor_kod", "sektor", "isletme_sayisi", "pay_yuzde", "ort_google_puan",
     "medyan_yorum", "toplam_yorum"],
    [[kod, g[0]["sektor"], len(g), round(len(g) * 100 / len(tr), 1),
      round(sum(p) / len(p), 2) if (p := [x for x in map(puan, g) if x]) else "",
      statistics.median([yorum(x) for x in g]), sum(yorum(x) for x in g)]
     for kod, g in sorted(sek.items(), key=lambda kv: -len(kv[1]))])

# ── il ─────────────────────────────────────────────────────────────────
il = defaultdict(list)
for r in tr:
    il[r["il"]].append(r)
yaz("ozet-il.csv", ["il", "isletme_sayisi", "ilce_sayisi", "ort_google_puan", "toplam_yorum"],
    [[ad, len(g), len({x["ilce"] for x in g if x["ilce"]}),
      round(sum(p) / len(p), 2) if (p := [x for x in map(puan, g) if x]) else "",
      sum(yorum(x) for x in g)]
     for ad, g in sorted(il.items(), key=lambda kv: -len(kv[1]))])

# ── ilce ───────────────────────────────────────────────────────────────
ilc = Counter((r["il"], r["ilce"]) for r in tr if r["ilce"])
yaz("ozet-ilce.csv", ["il", "ilce", "isletme_sayisi"],
    [[a, b, n] for (a, b), n in sorted(ilc.items(), key=lambda kv: -kv[1])])

# ── il x sektor ────────────────────────────────────────────────────────
adlar = {r["sektor_kod"]: r["sektor"] for r in tr}
ks = Counter((r["il"], r["sektor_kod"]) for r in tr)
yaz("ozet-il-sektor.csv", ["il", "sektor_kod", "sektor", "isletme_sayisi"],
    [[a, b, adlar[b], n] for (a, b), n in sorted(ks.items(), key=lambda kv: -kv[1])])

# ── ust duzey ozet ─────────────────────────────────────────────────────
puanlar = [x for x in map(puan, tr) if x]
yorumlar = [yorum(r) for r in tr]
ozet = json.load(open(os.path.join(VERI, "ozet.json"), encoding="utf-8"))
ozet["turkiye"].update({
    "isletme": len(tr),
    "il": len({r["il"] for r in tr}),
    "ilce": len({(r["il"], r["ilce"]) for r in tr if r["ilce"]}),
    "sektor": len({r["sektor_kod"] for r in tr}),
    "ortalama_google_puan": round(sum(puanlar) / len(puanlar), 2),
    "toplam_google_yorum": sum(yorumlar),
    "medyan_google_yorum": statistics.median(yorumlar),
    "puan_4_5_ve_uzeri": sum(1 for p in puanlar if p >= 4.5),
})
with open(os.path.join(VERI, "ozet.json"), "w", encoding="utf-8") as f:
    json.dump(ozet, f, ensure_ascii=False, indent=2)
print("  ozet.json guncellendi")
print("\nTamam.")
