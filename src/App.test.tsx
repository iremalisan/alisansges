import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import App from './App';
import { SAMPLE_PROJECT_NAME } from './domain/sampleProject';
import { NEGATIVE_VALUE_MESSAGE } from './domain/validation';

describe('GES Metraj Pro — PR-001 foundation', () => {
  it('renders the application shell and main sections', () => {
    render(<App />);

    expect(screen.getByText('GES Metraj Pro')).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'GES Malzeme Hesaplama Aracı' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Proje Bilgileri' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Panel ve Masa' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Ayak ve Beton' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Kablo Kanalı ve Kum' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Beton Köşk ve Bakır Pabuç' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Bims Duvar' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Malzeme Listesi' }),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Hesaplama motoru sonraki adımda eklenecek.'),
    ).toBeInTheDocument();
  });

  it('loads sample project input values when örnek proje is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );

    expect(screen.getByLabelText('Proje adı')).toHaveValue(SAMPLE_PROJECT_NAME);
    expect(screen.getByLabelText('Santral gücü')).toHaveValue(90);
    expect(screen.getByLabelText('Panel gücü')).toHaveValue(580);
    expect(screen.getByLabelText('Masa başına panel sayısı')).toHaveValue(28);
    expect(screen.getByLabelText('Kanal uzunluğu')).toHaveValue(12000);
    expect(screen.getByLabelText('Beton köşk adedi')).toHaveValue(18);
    expect(screen.getByLabelText('Duvar uzunluğu')).toHaveValue(120);
  });

  it('clears the form when Formu Temizle is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );
    expect(screen.getByLabelText('Proje adı')).toHaveValue(SAMPLE_PROJECT_NAME);

    await user.click(screen.getByRole('button', { name: 'Formu Temizle' }));

    expect(screen.getByLabelText('Proje adı')).toHaveValue('');
    expect(screen.getByLabelText('Santral gücü')).toHaveValue(null);
    expect(screen.getByLabelText('Panel gücü')).toHaveValue(null);
    expect(screen.getByLabelText('Masa başına panel sayısı')).toHaveValue(null);
  });

  it('rejects negative numeric input with a Turkish validation message', () => {
    render(<App />);

    const plantPower = screen.getByLabelText('Santral gücü');
    fireEvent.change(plantPower, { target: { value: '-5' } });

    expect(screen.getByRole('alert')).toHaveTextContent(NEGATIVE_VALUE_MESSAGE);
    expect(plantPower).toHaveValue(null);
  });
});
