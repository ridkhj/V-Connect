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

interface Letter {
  code: string;
  name: string;
  type: 'reciprocas' | 'nsl' | 'agradecimento';
  date: string;
  status: string;
}

interface ErrorResponse {
  success: false;
  error: string;
  details: string;
  errorType: 'FILE_NOT_FOUND' | 'NO_DATA' | 'VALIDATION_ERROR' | 'SERVER_ERROR';
}

interface SuccessResponse {
  success: true;
  data: Letter[];
  message: string;
}

type ApiResponse = ErrorResponse | SuccessResponse;

interface ApiError {
  response?: {
    data?: ErrorResponse;
  };
}

export default function Letters() {
  const [letters, setLetters] = useState<Letter[]>([]);
  const [filteredLetters, setFilteredLetters] = useState<Letter[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{message: string, type: string} | null>(null);
  const [selectedLetters, setSelectedLetters] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [selectedType, setSelectedType] = useState<Letter['type']>('reciprocas');

  const processUploadedFiles = async () => {
    try {
      await api.post('/process-files');
      await fetchLetters();
    } catch (error) {
      console.error('Erro ao processar arquivos:', error);
      setError({
        message: "Erro ao processar arquivos",
        type: "PROCESSING_ERROR"
      });
    }
  };

  const fetchLetters = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<ApiResponse>(`/get-letters/${selectedType}`);
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
        setLetters([]);
        setFilteredLetters([]);
        return;
      }

      setLetters(data.data) ;
      setFilteredLetters(data.data);
    } catch (error: unknown) {
      let errorMessage = 'Erro ao carregar as cartas';
      let errorType = 'SERVER_ERROR';

      const apiError = error as ApiError;
      if (apiError.response?.data) {
        errorMessage = `${apiError.response.data.error}: ${apiError.response.data.details}`;
        errorType = apiError.response.data.errorType || 'SERVER_ERROR';
      }

      setError({ message: errorMessage, type: errorType });
      setLetters([]);
      setFilteredLetters([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLetters();
  }, [selectedType]);

  useEffect(() => {
    const filtered = letters.filter(letter => 
      letter.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      letter.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      letter.status.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredLetters(filtered);
  }, [searchTerm, letters]);

  const handlePrintReport = async () => {
    if (selectedLetters.length === 0) {
      alert('Selecione pelo menos uma carta para imprimir');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const selectedData = letters
        .filter(letter => selectedLetters.includes(letter.code))
        .map(letter => ({
          code: letter.code,
          name: letter.name,
          type: letter.type,
          date: letter.date,
          status: letter.status
        }));

      const response = await api.post(`/get-letters-pdf/${selectedType}`, selectedData, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cartas-${selectedType}.pdf`);
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

  const handleSelectLetter = (code: string) => {
    setSelectedLetters(prev => 
      prev.includes(code) 
        ? prev.filter(c => c !== code)
        : [...prev, code]
    );
  };

  const handleSelectAll = () => {
    if (selectedLetters.length === filteredLetters.length) {
      setSelectedLetters([]);
    } else {
      setSelectedLetters(filteredLetters.map(letter => letter.code));
    }
  };

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, { bg: string; text: string }> = {
      'Pendente': { bg: 'bg-yellow-50', text: 'text-yellow-700' },
      'Enviado': { bg: 'bg-green-50', text: 'text-green-700' },
      'Em Processamento': { bg: 'bg-blue-50', text: 'text-blue-700' },
      'Cancelado': { bg: 'bg-red-50', text: 'text-red-700' }
    };

    return statusColors[status] || { bg: 'bg-gray-50', text: 'text-gray-700' };
  };

  const getTypeLabel = (type: Letter['type']) => {
    const types = {
      'reciprocas': 'Recíprocas',
      'nsl': 'NSL',
      'agradecimento': 'Agradecimento'
    };
    return types[type];
  };

  const renderError = () => {
    const errorColors = {
      FILE_NOT_FOUND: 'text-yellow-600 bg-yellow-50 border-yellow-200',
      NO_DATA: 'text-orange-600 bg-orange-50 border-orange-200',
      VALIDATION_ERROR: 'text-red-600 bg-red-50 border-red-200',
      SERVER_ERROR: 'text-red-600 bg-red-50 border-red-200'
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
            <h1 className="text-xl font-bold text-gray-800">Relatório de Cartas</h1>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">
              {selectedLetters.length} de {filteredLetters.length} selecionados
            </span>
          </div>
        </header>

        <div className="p-6">
          <div className="flex gap-2 mb-6">
            {(['reciprocas', 'nsl', 'agradecimento'] as const).map((type) => (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                  selectedType === type
                    ? 'bg-indigo-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
                }`}
              >
                {getTypeLabel(type)}
              </button>
            ))}
          </div>

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
                disabled={selectedLetters.length === 0 || isGeneratingPDF}
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
                        checked={selectedLetters.length === filteredLetters.length && filteredLetters.length > 0}
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
                  {filteredLetters.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="text-center py-8 text-gray-500">
                        Nenhum registro encontrado
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredLetters.map((letter, index) => (
                      <TableRow 
                        key={index}
                        className="hover:bg-gray-50 transition-colors"
                      >
                        <TableCell className="text-center">
                          <input 
                            type="checkbox"
                            checked={selectedLetters.includes(letter.code)}
                            onChange={() => handleSelectLetter(letter.code)}
                            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </TableCell>
                        <TableCell className="font-medium text-gray-900">{letter.code}</TableCell>
                        <TableCell className="text-gray-700">{letter.name}</TableCell>
                        <TableCell>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            getStatusColor(letter.status).bg
                          } ${getStatusColor(letter.status).text}`}>
                            {letter.status}
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
