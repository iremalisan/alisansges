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

## PR-002 kapsamı

- Saf fonksiyonlarla hesaplama motoru
- Masa ve beton köşk reçete sistemi
- Canlı özet kartlar ve malzeme sonuç tablosu
- Aynı malzeme kimliğinin tek satırda birleştirilmesi

## PR-003 kapsamı

- Çoklu kablo kanalı satırları
- Çoklu köşk grupları
- Çoklu yapı/duvar satırları
- Satır ekleme / silme / kopyalama
- Satır bazlı doğrulama
- Tüm satırların malzeme sonuçlarında toplanması

### PR-003 formülleri

- Kazı: `uzunluk × genişlik × derinlik`
- Alt/üst kum: `uzunluk × genişlik × kumYüksekliği`
- Sipariş kum: `netKum × (1 + fire/100)`
- Sipariş kablo: `kabloUzunluğu × (1 + fire/100)` (tip → malzeme kimliği)
- Uyarı bandı / plaka / boru: `uzunluk × hatAdedi`
- Köşk grubu: `adet × görünürBirimMiktar` (gruplar toplanır)
- Duvar bims: `ceil(netAlan / (genişlik × yükseklik))`, fire ile sipariş

### Çoklu girdi davranışı

- Kanal, köşk ve duvar koleksiyonları boş başlayabilir.
- Örnek proje birden fazla satır yükler.
- Aynı `MaterialId` tek satırda birleşir; açıklamalar kaynakları özetler.
- Geçersiz bir satır diğer geçerli satırların hesabını bozmaz.

### Reçete uyarısı

Hazır reçeteler örnek başlangıç değerleridir. Gerçek proje standartlarınıza göre kontrol ediniz.

### Bilinen sınırlamalar

- Genel proje fire oranı küresel uygulanmaz.
- Reçete editörü yoktur.
- Excel dışa aktarma ve yerel proje kaydı yoktur.

## Sonraki planlanan PR

Excel dışa aktarma ve yerel proje kalıcılığı.
