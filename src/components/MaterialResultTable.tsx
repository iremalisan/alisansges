import type { MaterialResultRow } from '../domain/types';
import './MaterialResultTable.css';

interface MaterialResultTableProps {
  rows: MaterialResultRow[];
}

function formatCell(value: number | null): string {
  if (value === null || value === undefined) {
    return '—';
  }

  return new Intl.NumberFormat('tr-TR', {
    maximumFractionDigits: 3,
  }).format(value);
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
                Henüz malzeme satırı yok. Hesaplama motoru sonraki adımda eklenecek.
              </td>
            </tr>
          ) : (
            rows.map((row) => (
              <tr key={row.id}>
                <td>{row.category}</td>
                <td>{row.material}</td>
                <td>{formatCell(row.calculatedQuantity)}</td>
                <td>{row.unit}</td>
                <td>
                  {row.wasteRatePercent === null
                    ? '—'
                    : `% ${formatCell(row.wasteRatePercent)}`}
                </td>
                <td>{formatCell(row.orderQuantity)}</td>
                <td>{row.calculationNote || '—'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
