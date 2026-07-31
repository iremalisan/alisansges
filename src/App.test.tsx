import { fireEvent, render, screen, within } from '@testing-library/react';
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
  });

  it('loads sample project input values when örnek proje is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );

    expect(screen.getByLabelText('Proje adı')).toHaveValue(SAMPLE_PROJECT_NAME);
    expect(screen.getByLabelText('Santral gücü')).toHaveValue(90);
    expect(screen.getByLabelText('Panel gücü')).toHaveValue(700);
    expect(screen.getByLabelText('Masa başına panel sayısı')).toHaveValue(56);
    expect(screen.getByDisplayValue('DC Ana Kanal')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Ana Köşkler')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Ana Köşk Duvarı')).toBeInTheDocument();
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
    expect(screen.getByText(/Henüz kanal yok/i)).toBeInTheDocument();
  });

  it('rejects negative numeric input with a Turkish validation message', () => {
    render(<App />);

    const plantPower = screen.getByLabelText('Santral gücü');
    fireEvent.change(plantPower, { target: { value: '-5' } });

    expect(screen.getByRole('alert')).toHaveTextContent(NEGATIVE_VALUE_MESSAGE);
    expect(plantPower).toHaveValue(null);
  });
});

describe('GES Metraj Pro — PR-002 / PR-003 calculations', () => {
  it('shows live panel count for the 90 MWp example', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );

    const panelCard = screen.getByRole('article', { name: 'Panel' });
    expect(within(panelCard).getByText('128.572')).toBeInTheDocument();
    expect(screen.getAllByText(/ceil\(90 MWp/).length).toBeGreaterThan(0);
  });

  it('shows recipe warning text', () => {
    render(<App />);
    expect(
      screen.getAllByText(/Hazır reçeteler örnek başlangıç değerleridir/i)
        .length,
    ).toBeGreaterThan(0);
  });

  it('resets calculated results with Formu Temizle', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );
    expect(
      within(screen.getByRole('article', { name: 'Panel' })).getByText(
        '128.572',
      ),
    ).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Formu Temizle' }));

    expect(
      within(screen.getByRole('article', { name: 'Panel' })).getByText('—'),
    ).toBeInTheDocument();
  });

  it('adds, duplicates and removes trench rows', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole('button', { name: 'Kanal Ekle' }));
    expect(screen.getByDisplayValue('Yeni Kanal')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Kopyala' }));
    expect(screen.getByDisplayValue('Yeni Kanal (Kopya)')).toBeInTheDocument();

    const removeButtons = screen.getAllByRole('button', { name: 'Sil' });
    await user.click(removeButtons[0]);
    expect(screen.queryByDisplayValue('Yeni Kanal')).not.toBeInTheDocument();
    expect(screen.getByDisplayValue('Yeni Kanal (Kopya)')).toBeInTheDocument();
  });

  it('loads multi-row example content', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole('button', { name: '90 MWp Örnek Proje' }),
    );

    expect(screen.getByDisplayValue('DC Ana Kanal')).toBeInTheDocument();
    expect(screen.getByDisplayValue('OG Ana Kanal')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Haberleşme Kanalı')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Ana Köşkler')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Yardımcı Köşkler')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Ana Köşk Duvarı')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Depo Duvarı')).toBeInTheDocument();
  });
});
