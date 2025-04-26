import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Cards from '@/pages/cards'

describe('Cards', () => {
  it('renderiza o título do relatório', () => {
    render(
      <MemoryRouter>
        <Cards />
      </MemoryRouter>
    );

    expect(screen.getByText(/Relatório de Cartas/i)).toBeInTheDocument();
  });

  it('renderiza botões de imprimir e enviar email', () => {
    render(
      <MemoryRouter>
        <Cards />
      </MemoryRouter>
    );

    expect(screen.getByText(/Imprimir Relatório/i)).toBeInTheDocument();
    expect(screen.getByText(/Enviar Email/i)).toBeInTheDocument();
  });

  it('renderiza a tabela com pessoas', () => {
    render(
      <MemoryRouter>
        <Cards />
      </MemoryRouter>
    );

    // Verifica se os nomes estão na tabela
    expect(screen.getByText('Edson Alves da Silva')).toBeInTheDocument();
    expect(screen.getByText('Wedne Morais de Araújo')).toBeInTheDocument();
    
    // Verifica se o estado está presente
    expect(screen.getAllByText('PB').length).toBeGreaterThan(0);
  });

  it('renderiza checkboxes na tabela', () => {
    render(
      <MemoryRouter>
        <Cards />
      </MemoryRouter>
    );

    const checkboxes = screen.getAllByRole('checkbox');
    expect(checkboxes.length).toBeGreaterThan(0);
  });

  it('possui link de voltar para a página inicial', () => {
    render(
      <MemoryRouter>
        <Cards />
      </MemoryRouter>
    );

    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/');
  });
});
