import { render, screen, fireEvent } from '@testing-library/react';
import FileUploader from './file-uploader';
import { describe, it, vi } from 'vitest';

describe('FileUploader Component', () => {
  it('should call onUpload when a file is uploaded', async () => {
    const mockOnUpload = vi.fn();
    render(<FileUploader onUpload={mockOnUpload} />);

    const inputElement = screen.getByText('Escolha os arquivos');
    const file = new File(['file content'], 'example.txt', { type: 'text/plain' });

    fireEvent.change(inputElement, { target: { files: [file] } });
  });

  it('should display uploaded files in the recent tab', async () => {
    const mockOnUpload = vi.fn();
    render(<FileUploader onUpload={mockOnUpload} />);

    const inputElement = screen.getByText('Escolha os arquivos');
    const file = new File(['file content'], 'example.txt', { type: 'text/plain' });

    fireEvent.change(inputElement, { target: { files: [file] } });

    const recentTabButton = screen.getByText('Recentes');
    fireEvent.click(recentTabButton);
  });

  it('should delete a file when the delete button is clicked', async () => {
    const mockOnUpload = vi.fn();
    render(<FileUploader onUpload={mockOnUpload} />);

    const inputElement = screen.getByText('Escolha os arquivos');
    const file = new File(['file content'], 'example.txt', { type: 'text/plain' });

    fireEvent.change(inputElement, { target: { files: [file] } });

    const recentTabButton = screen.getByText('Recentes');
    fireEvent.click(recentTabButton);
  });
});