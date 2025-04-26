import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Options from './options'

describe('Options', () => {
  it('renderiza os textos corretamente', () => {
    render(
      <MemoryRouter>
        <Options />
      </MemoryRouter>
    );

    expect(screen.getByRole('heading', { name: /Relatório de Atualizações/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Relatório de CDPR´S/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Relatório de Cartas/i })).toBeInTheDocument();

    expect(screen.getByText(/45 vencidas/i)).toBeInTheDocument();
    expect(screen.getAllByText(/7 vencidas, 4 a fazer/i)).toHaveLength(2);
  });

  it('tem links corretos', () => {
    render(
      <MemoryRouter>
        <Options />
      </MemoryRouter>
    );

    const links = screen.getAllByRole('link');
    expect(links[0]).toHaveAttribute('href', '/updates');
    expect(links[1]).toHaveAttribute('href', '/cdprs');
    expect(links[2]).toHaveAttribute('href', '/cards');
  });
});
