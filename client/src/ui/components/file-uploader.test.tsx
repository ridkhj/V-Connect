import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import FileUploader from './file-uploader'

describe('FileUploader', () => {
  it('renderiza os botões de tabs', () => {
    render(<FileUploader />);

    expect(screen.getByRole('button', { name: /fazer upload/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /recentes/i })).toBeInTheDocument();
  });

  it('mostra área de upload por padrão', () => {
    render(<FileUploader />);

    expect(screen.getByText(/Arraste e solte seus arquivos/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Escolha os arquivos/i })).toBeInTheDocument();
  });

  it('troca para aba de recentes ao clicar', () => {
    render(<FileUploader />);

    const recentTabButton = screen.getByRole('button', { name: /recentes/i });
    fireEvent.click(recentTabButton);

    expect(screen.getByText(/Nenhum arquivo carregado ainda/i)).toBeInTheDocument();
  });

  it('chama onUpload quando arquivo é selecionado', () => {
    const onUploadMock = vi.fn();
    render(<FileUploader onUpload={onUploadMock} />);
  
    const file = new File(['conteúdo'], 'teste.csv', { type: 'text/csv' });
    const input = document.getElementById('file-input') as HTMLInputElement;
  
    fireEvent.change(input, { target: { files: [file] } });
  
    expect(onUploadMock).toHaveBeenCalledTimes(1);
    expect(onUploadMock).toHaveBeenCalledWith(file);
  });
});
