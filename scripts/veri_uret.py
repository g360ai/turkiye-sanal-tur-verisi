#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ham G360 kaydindan yayin veri setini uretir.

Kullanim:  python scripts/veri_uret.py <ham.json>

Ham kayit yalnizca G360'in kendi uretim veritabanidir. Bu script,
yayinlanabilir alanlari secer; kisisel/iletisim verisini disarida birakir.
"""
import csv
import io
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERI = os.path.join(KOK, "data")

# Yayinlanmayan ham alanlar (bilerek disarida):
#   adres, telefon, website, yorumlar, calismaSaatleri, photos, turSifresi,
#   thumbnailUrl, oncelik*, vitpi*, menuOptions, serviceOptions, accessibility
YAYIN_DISI = {
    "adres", "telefon", "website", "yorumlar", "calismaSaatleri", "photos",
    "turSifresi", "thumbnailUrl", "menuOptions", "serviceOptions",
    "accessibility", "ozellikler", "priceLevel", "priceLevelRaw",
}

# Kanada bolgeleri (ulke tespiti icin)
CA_BOLGE = {"Alberta", "Saskatchewan"}

# Onceki surumde olmayan sektor kodlari icin ad
YENI_SEKTOR_AD = {"turistik": "Turistik Yer"}

ALANLAR = [
    "id", "ad", "ulke", "il", "ilce", "sektor_kod", "sektor",
    "google_puan", "google_yorum_sayisi", "enlem", "boylam",
    "google_cid", "google_place_id", "tur_url",
    # 2026.10 ile eklenenler
    "sektor_etiketleri", "sahne_sayisi", "street_view_var",
    "cekim_yili", "yayin_yili",
]


def sektor_adlari():
    """Onceki surumun kod -> ad eslemesini korur."""
    ad = dict(YENI_SEKTOR_AD)
    yol = os.path.join(VERI, "ozet-sektor.csv")
    if os.path.exists(yol):
        with io.open(yol, encoding="utf-8") as f:
            for s in csv.DictReader(f):
                ad.setdefault(s["sektor_kod"], s["sektor"])
    return ad


def yil(deger):
    if isinstance(deger, str) and len(deger) >= 4 and deger[:4].isdigit():
        return int(deger[:4])
    return None


def sayi(deger):
    if isinstance(deger, bool) or deger in (None, ""):
        return None
    try:
        return float(deger)
    except (TypeError, ValueError):
        return None


def donustur(ham, ad_haritasi):
    etiketler = [p.strip() for p in (ham.get("kategori") or "").split(",") if p.strip()]
    kod = etiketler[0] if etiketler else "diger"
    koord = ham.get("koordinatlar") or {}
    puan = sayi(ham.get("puan"))
    yorum = sayi(ham.get("yorumSayisi"))
    lat = sayi(koord.get("lat"))
    lng = sayi(koord.get("lng"))
    return {
        "id": ham.get("id"),
        "ad": ham.get("ad"),
        "ulke": "CA" if ham.get("il") in CA_BOLGE else "TR",
        "il": ham.get("il"),
        "ilce": ham.get("ilce"),
        "sektor_kod": kod,
        "sektor": ad_haritasi.get(kod, kod.title()),
        "google_puan": round(puan, 1) if puan is not None else None,
        "google_yorum_sayisi": int(yorum) if yorum is not None else None,
        "enlem": lat,
        "boylam": lng,
        "google_cid": ham.get("cid") or None,
        "google_place_id": ham.get("placeId") or None,
        "tur_url": "https://g360.ai/vr/%s" % ham.get("id"),
        "sektor_etiketleri": etiketler,
        "sahne_sayisi": int(ham["sahneSayisi"]) if isinstance(ham.get("sahneSayisi"), (int, float)) and ham.get("sahneSayisi") else None,
        "street_view_var": bool(ham.get("streetViewEmbed")),
        "cekim_yili": yil(ham.get("cekimTarihi")),
        "yayin_yili": yil(ham.get("yayinTarihi")),
    }


def csv_deger(alan, deger):
    if deger is None:
        return ""
    if alan == "sektor_etiketleri":
        return "|".join(deger)
    if alan == "street_view_var":
        return "1" if deger else "0"
    return deger


def main():
    if len(sys.argv) < 2:
        sys.exit("kullanim: python scripts/veri_uret.py <ham.json>")
    with io.open(sys.argv[1], encoding="utf-8") as f:
        ham = json.load(f)
    if isinstance(ham, dict):
        ham = ham.get("isletmeler", [])

    ad_haritasi = sektor_adlari()
    kayitlar = [donustur(h, ad_haritasi) for h in ham if h.get("id")]
    kayitlar.sort(key=lambda r: r["id"])

    # Gizlilik denetimi: yayin disi alan sizmasin
    for r in kayitlar:
        sizan = YAYIN_DISI & set(r)
        if sizan:
            sys.exit("HATA: yayin disi alan ciktida: %s" % sorted(sizan))

    with io.open(os.path.join(VERI, "isletmeler.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(kayitlar, f, ensure_ascii=False, indent=1)
        f.write("\n")

    with io.open(os.path.join(VERI, "isletmeler.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(ALANLAR)
        for r in kayitlar:
            w.writerow([csv_deger(a, r[a]) for a in ALANLAR])

    ozellikler = []
    for r in kayitlar:
        if r["enlem"] is None or r["boylam"] is None:
            continue
        nitelik = {a: r[a] for a in ALANLAR if a not in ("enlem", "boylam")}
        ozellikler.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [r["boylam"], r["enlem"]]},
            "properties": nitelik,
        })
    with io.open(os.path.join(VERI, "isletmeler.geojson"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"type": "FeatureCollection", "features": ozellikler}, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("isletmeler.json / .csv : %d kayit" % len(kayitlar))
    print("isletmeler.geojson     : %d nokta" % len(ozellikler))


if __name__ == "__main__":
    main()
