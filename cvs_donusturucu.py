import csv
import json
import os
import chardet
from pprint import pprint


def dosya_kodlamasi_bul(dosya_adi):
    with open(dosya_adi, 'rb') as f:
        sonuc = chardet.detect(f.read(1024))
    return sonuc['encoding'] or 'utf-8'


def csv_oku_genel(dosya_adi):
    if not os.path.exists(dosya_adi):
        raise FileNotFoundError(f"Dosya bulunamadı: {dosya_adi}")

    kodlama = dosya_kodlamasi_bul(dosya_adi)

    with open(dosya_adi, 'r', encoding=kodlama, newline='') as f:
        ornek = f.read(2048)
        f.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(ornek)
        except csv.Error:
            dialect = csv.excel

        okuyucu = csv.DictReader(f, dialect=dialect)
        veriler = [satir for satir in okuyucu]
        return veriler


def csv_to_json(dosya_adi):
    veriler = csv_oku_genel(dosya_adi)
    return json.dumps(veriler, indent=4, ensure_ascii=False)


def main():
    dosya_adi = input("CSV dosya yolunu girin: ")
    try:
        veriler = csv_oku_genel(dosya_adi)
        print("\nCSV Verisi:")
        pprint(veriler)

        print("\nJSON Formatı:")
        print(csv_to_json(dosya_adi))

    except Exception as e:
        print(f"Hata: {e}")


if __name__ == "__main__":
    main()
