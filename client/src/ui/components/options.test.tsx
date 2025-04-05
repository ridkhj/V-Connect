import { render, screen } from '@testing-library/react';
import Options from './options';

describe('Options Component', () => {
  it('should render the main container', () => {
    render(<Options />);
    const mainElement = screen.getByRole('main');
    expect(mainElement).toBeInTheDocument();
  });

  it('should render three buttons', () => {
    render(<Options />);
    const buttons = screen.getAllByRole('button');
    expect(buttons).toHaveLength(3);
  });

  it('should render the correct titles for each button', () => {
    render(<Options />);
    expect(screen.getByText('Relatório de Atualizações')).toBeInTheDocument();
    expect(screen.getByText('Relatório de CDPR´S')).toBeInTheDocument();
    expect(screen.getByText('Relatório de Cartas')).toBeInTheDocument();
  });
});