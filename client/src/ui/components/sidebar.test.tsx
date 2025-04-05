import { render, screen } from '@testing-library/react';
import Sidebar from './sidebar';

describe('Sidebar Component', () => {
  it('should render the logo with correct alt text', () => {
    render(<Sidebar />);
    const logo = screen.getByAltText('Logo');
    expect(logo).toBeInTheDocument();
  });

  it('should render the title "Connect"', () => {
    render(<Sidebar />);
    const title = screen.getByText('Connect');
    expect(title).toBeInTheDocument();
  });

  it('should render the FileUploader component', () => {
    render(<Sidebar />);
    const fileUploader = screen.getByText(/upload/i);
    expect(fileUploader).toBeInTheDocument();
  });

  it('should render the footer with copyright text', () => {
    render(<Sidebar />);
    const footerText = screen.getByText(/© 20025 V Connect \| Todos os direitos reservados\./i);
    expect(footerText).toBeInTheDocument();
  });
});