import './UnitLabel.css';

interface UnitLabelProps {
  unit: string;
}

export function UnitLabel({ unit }: UnitLabelProps) {
  return <span className="unit-label">{unit}</span>;
}
