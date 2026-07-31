import type { MaterialResultRow } from '../domain/types';
import './MaterialResultTable.css';

interface MaterialResultTableProps {
  rows: MaterialResultRow[];
}

function formatQuantity(value: number | null, unit: string): string {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return '—';
  }

  const decimals = unit === 'm³' || unit === 'm²' || unit === 'm' ? 3 : 0;

  return new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

function formatPercent(value: number | null): string {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return '—';
  }

  return `% ${new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value)}`;
}

export function MaterialResultTable({ rows }: MaterialResultTableProps) {
  return (
    <div className="material-table-wrap">
      <table className="material-table">
        <thead>
          <tr>
            <th scope="col">Kategori</th>
            <th scope="col">Malzeme</th>
            <th scope="col">Hesaplanan Miktar</th>
            <th scope="col">Birim</th>
            <th scope="col">Fire Oranı</th>
            <th scope="col">Sipariş Miktarı</th>
            <th scope="col">Hesap Açıklaması</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={7} className="material-table__empty">
                Hesaplama için gerekli girdileri doldurun. Sonuçlar otomatik
                güncellenir.
              </td>
            </tr>
          ) : (
            rows.map((row) => (
              <tr key={row.id}>
                <td>{row.category}</td>
                <td>{row.material}</td>
                <td>{formatQuantity(row.calculatedQuantity, row.unit)}</td>
                <td>{row.unit}</td>
                <td>{formatPercent(row.wasteRatePercent)}</td>
                <td>{formatQuantity(row.orderQuantity, row.unit)}</td>
                <td>{row.calculationNote || '—'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
