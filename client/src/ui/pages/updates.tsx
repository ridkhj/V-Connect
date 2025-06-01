import { useState, useEffect } from "react";
import { Link } from "react-router-dom"
import { ArrowLeft, Search, Download, Loader2, AlertCircle } from "lucide-react"
import Sidebar from "@/components/sidebar"
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table"
import { api } from "@/services/api";

interface Update {
  code: string;
  name: string;
  status: string;
}

interface ErrorResponse {
  success: false;
  error: string;
  details: string;
  errorType: 'FILE_NOT_FOUND' | 'NO_DATA' | 'VALIDATION_ERROR' | 'SERVER_ERROR' | 'PROCESSING_ERROR';
}

interface SuccessResponse {
  success: true;
  data: Update[];
  message: string;
}

type ApiResponse = ErrorResponse | SuccessResponse;

interface ApiError {
  response?: {
    data?: ErrorResponse;
  };
}

export default function Updates() {
  const [updates, setUpdates] = useState<Update[]>([]);
  const [filteredUpdates, setFilteredUpdates] =  useState<Update[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{message: string, type: string} | null>(null);
  const [selectedUpdates, setSelectedUpdates] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);

  const processUploadedFiles = async () => {
    try {
      await api.post('/process-files');
      await fetchUpdates();
    } catch (error) {
      console.error('Erro ao processar arquivos:', error);
      setError({
        message: "Erro ao processar arquivos",
        type: "PROCESSING_ERROR"
      });
    }
  };

  const fetchUpdates = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<ApiResponse>('/get-updates');
      const data = response.data;

      if (!data.success) {
        if (data.errorType === "FILE_NOT_FOUND") {
          await processUploadedFiles();
          return;
        }
        
        setError({
          message: `${data.error}: ${data.details}`,
          type: data.errorType
        });
        setUpdates([]);
        setFilteredUpdates([]);
        return;
      }

      setUpdates(data.data);
      setFilteredUpdates(data.data);
    } catch (error: unknown) {
      let errorMessage = 'Erro ao carregar as atualizações';
      let errorType = 'SERVER_ERROR';

      const apiError = error as ApiError;
      if (apiError.response?.data) {
        errorMessage = `${apiError.response.data.error}: ${apiError.response.data.details}`;
        errorType = apiError.response.data.errorType || 'SERVER_ERROR';
      }

      setError({ message: errorMessage, type: errorType });
      setUpdates([]);
      setFilteredUpdates([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUpdates();
  }, []);

  useEffect(() => {
    const filtered = updates.filter(update => 
      update.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      update.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      update.status.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredUpdates(filtered);
  }, [searchTerm, updates]);

  const handlePrintReport = async () => {
    if (selectedUpdates.length === 0) {
      alert('Selecione pelo menos uma atualização para imprimir');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const selectedData = updates
        .filter(update => selectedUpdates.includes(update.code))
        .map(update => ({
          code: update.code,
          name: update.name,
          status: update.status
        }));

      const response = await api.post('/get-updates-pdf', selectedData, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'atualizacoes.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erro ao gerar PDF:', error);
      alert('Erro ao gerar o relatório PDF');
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  const handleSelectUpdate = (code: string) => {
    setSelectedUpdates(prev => 
      prev.includes(code) 
        ? prev.filter(c => c !== code)
        : [...prev, code]
    );
  };

  const handleSelectAll = () => {
    if (selectedUpdates.length === filteredUpdates.length) {
      setSelectedUpdates([]);
    } else {
      setSelectedUpdates(filteredUpdates.map(update => update.code));
    }
  };

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, { bg: string; text: string }> = {
      'Pendente': { bg: 'bg-yellow-50', text: 'text-yellow-700' },
      'Concluído': { bg: 'bg-green-50', text: 'text-green-700' },
      'Em Andamento': { bg: 'bg-blue-50', text: 'text-blue-700' },
      'Cancelado': { bg: 'bg-red-50', text: 'text-red-700' }
    };

    return statusColors[status] || { bg: 'bg-gray-50', text: 'text-gray-700' };
  };

  const renderError = () => {
    const errorColors = {
      FILE_NOT_FOUND: 'text-yellow-600 bg-yellow-50 border-yellow-200',
      NO_DATA: 'text-orange-600 bg-orange-50 border-orange-200',
      VALIDATION_ERROR: 'text-red-600 bg-red-50 border-red-200',
      SERVER_ERROR: 'text-red-600 bg-red-50 border-red-200',
      PROCESSING_ERROR: 'text-red-600 bg-red-50 border-red-200'
    };

    const color = errorColors[error?.type as keyof typeof errorColors] || errorColors.SERVER_ERROR;

    return (
      <div className={`flex items-center gap-2 p-4 rounded-lg border ${color}`}>
        <AlertCircle className="h-5 w-5" />
        <p className="text-sm">
          {error?.message}
        </p>
      </div>
    );
  };

  return (
    <div className="w-screen h-screen flex overflow-x-hidden">
      <Sidebar />

      <div className="ml-[25%] w-full bg-zinc-50">
        <header className="flex justify-between items-center p-6 bg-white border-b border-gray-200 shadow-sm">
          <div className="flex items-center gap-4">
            <Link to="/" className="hover:bg-gray-100 p-2 rounded-full transition-colors">
              <ArrowLeft size={24} className="text-black" />
            </Link>
            <h1 className="text-xl font-bold text-gray-800">Relatório de Atualizações</h1>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">
              {selectedUpdates.length} de {filteredUpdates.length} selecionados
            </span>
          </div>
        </header>

        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-4 flex-1 max-w-md">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Buscar por código, nome ou status..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <button
                onClick={handlePrintReport}
                disabled={selectedUpdates.length === 0 || isGeneratingPDF}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGeneratingPDF ? (
                  <Loader2 className="animate-spin" size={18} />
                ) : (
                  <Download size={18} />
                )}
                Gerar PDF
              </button>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="animate-spin text-indigo-600" size={32} />
            </div>
          ) : error ? (
            <div className="flex justify-center items-center h-64">
              {renderError()}
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <Table>
                <TableHeader>
                  <TableRow className="bg-zinc-200">
                    <TableHead className="w-[50px] text-center">
                      <input 
                        type="checkbox"
                        checked={selectedUpdates.length === filteredUpdates.length && filteredUpdates.length > 0}
                        onChange={handleSelectAll}
                        className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </TableHead>
                    <TableHead className="font-semibold text-gray-700">Código</TableHead>
                    <TableHead className="font-semibold text-gray-700">Nome</TableHead>
                    <TableHead className="font-semibold text-gray-700">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUpdates.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-center py-8 text-gray-500">
                        Nenhum registro encontrado
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredUpdates.map((update, index) => (
                      <TableRow 
                        key={index}
                        className="hover:bg-gray-50 transition-colors"
                      >
                        <TableCell className="text-center">
                          <input 
                            type="checkbox"
                            checked={selectedUpdates.includes(update.code)}
                            onChange={() => handleSelectUpdate(update.code)}
                            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </TableCell>
                        <TableCell className="font-medium text-gray-900">{update.code}</TableCell>
                        <TableCell className="text-gray-700">{update.name}</TableCell>
                        <TableCell>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            getStatusColor(update.status).bg
                          } ${getStatusColor(update.status).text}`}>
                            {update.status}
                          </span>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
