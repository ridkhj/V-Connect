import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Updates from '@/pages/updates'

describe('Updates', () => {
  it('deve renderizar o título do relatório', () => {
    render(
      <MemoryRouter>
        <Updates />
      </MemoryRouter>
    );
    expect(screen.getByText(/relatório de atualizações/i)).toBeInTheDocument();
  });

  it('deve renderizar o botão fixo de cópia', () => {
    render(
      <MemoryRouter>
        <Updates />
      </MemoryRouter>
    );
    expect(screen.getByLabelText(/copiar/i)).toBeInTheDocument();
  });
});
