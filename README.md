# GES Metraj Pro

Yerel çalışan bir GES (Güneş Enerji Santrali) malzeme miktarı hesaplama aracı.

Bu uygulama bağımsızdır; başka bir projeye bağlı değildir.

## Kurulum

```bash
npm install
```

## Yerel çalıştırma

```bash
npm run dev
```

## Test

```bash
npm test
```

## Üretim derlemesi

```bash
npm run build
```

## PR-001 kapsamı

- Vite + React + TypeScript iskeleti
- Masaüstü öncelikli düzen ve sol bölüm navigasyonu
- Türkçe arayüz metinleri
- Form bölümleri ve yeniden kullanılabilir bileşenler
- Tip güvenli girdi modelleri

## PR-002 kapsamı

- Saf fonksiyonlarla hesaplama motoru
- Masa ve beton köşk reçete sistemi
- Canlı özet kartlar ve malzeme sonuç tablosu
- Aynı malzeme kimliğinin tek satırda birleştirilmesi
- Formül doğrulama ve otomatik testler

### Uygulanan formüller

- Panel: `ceil(santralMWp × 1.000.000 / panelWp)`
- Masa: `ceil(panelAdedi / masaBaşınaPanel)`
- Toplam ayak: `masaAdedi × masaBaşınaAyak`
- Beton ayak (yüzde): `ceil(toplamAyak × oran / 100)`
- Beton hacmi: ayak × (genişlik × uzunluk × derinlik), sipariş = net × (1 + fire/100)
- Kum: kanal × genişlik × yükseklik, sipariş = net × (1 + fire/100)
- Köşk malzemeleri: `köşkAdedi × köşkBaşınaMiktar`
- Bims (duvar): `ceil(netAlan / (bimsGenişlik × bimsYükseklik))`, sipariş fire ile yukarı yuvarlanır
- Reçete malzemeleri: `masaAdedi × masaBaşınaMiktar`

### Reçete sistemi

- Masa reçeteleri (`2P x 14`, `2P x 28`) mekanik malzeme miktarlarını tanımlar.
- Köşk reçeteleri (`Standart Beton Köşk`, `Büyük Beton Köşk`) birim başına elektrik/inşaat malzemelerini tanımlar.
- Reçete seçimi alanları doldurur; kullanıcı değerleri elle değiştirebilir.
- **Uyarı:** Hazır reçeteler örnek başlangıç değerleridir. Gerçek proje standartlarınıza göre kontrol ediniz.

### Bilinen sınırlamalar

- Genel proje fire oranı henüz küresel uygulanmaz (sonraki adım için ayrılmıştır).
- Kablo kanalı tek satırlıdır; çoklu hat / kablo metrajı yoktur.
- Reçete editörü yoktur; starter reçeteler kod içindedir.

## Sonraki planlanan PR

Çok satırlı kablo kanalı ve kablo hesaplamaları.
