import { useState, useEffect } from "react";
import { Link } from "react-router-dom"
import { ArrowLeft, Search, Download, Loader2, AlertCircle } from "lucide-react"
import Sidebar from "../components/sidebar"
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "../components/ui/table"
import { api } from "../services/api";

interface CDPR {
  code: string;
  name: string;
  age: string;
}

interface ErrorResponse {
  success: false;
  error: string;
  details: string;
  errorType: 'FILE_NOT_FOUND' | 'NO_DATA' | 'VALIDATION_ERROR' | 'SERVER_ERROR' | 'PROCESSING_ERROR';
}

interface SuccessResponse {
  success: true;
  data: CDPR[];
  message: string;
}

type ApiResponse = ErrorResponse | SuccessResponse;

interface ApiError {
  response?: {
    data?: ErrorResponse;
  };
}

export default function Cdprs() {
  const [cdprs, setCdprs] = useState<CDPR[]>([]);
  const [filteredCdprs, setFilteredCdprs] = useState<CDPR[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{message: string, type: string} | null>(null);
  const [selectedCdprs, setSelectedCdprs] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);

  const processUploadedFiles = async () => {
    try {
      await api.post('/process-files');
      await fetchCdprs();
    } catch (error) {
      console.error('Erro ao processar arquivos:', error);
      setError({
        message: "Erro ao processar arquivos",
        type: "PROCESSING_ERROR"
      });
    }
  };

  const fetchCdprs = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<ApiResponse>('/get-cdpr');
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
        setCdprs([]);
        setFilteredCdprs([]);
        return;
      }

      setCdprs(data.data);
      setFilteredCdprs(data.data);
    } catch (error: unknown) {
      let errorMessage = 'Erro ao carregar os dados do CDPR';
      let errorType = 'SERVER_ERROR';

      const apiError = error as ApiError;
      if (apiError.response?.data) {
        errorMessage = `${apiError.response.data.error}: ${apiError.response.data.details}`;
        errorType = apiError.response.data.errorType || 'SERVER_ERROR';
      }

      setError({ message: errorMessage, type: errorType });
      setCdprs([]);
      setFilteredCdprs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCdprs();
  }, []);

  useEffect(() => {
    const filtered = cdprs.filter(cdpr => 
      cdpr.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cdpr.code.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredCdprs(filtered);
  }, [searchTerm, cdprs]);

  const handlePrintReport = async () => {
    if (selectedCdprs.length === 0) {
      alert('Selecione pelo menos um CDPR para imprimir');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const selectedData = cdprs
        .filter(cdpr => selectedCdprs.includes(cdpr.code))
        .map(cdpr => ({
          code: cdpr.code,
          name: cdpr.name,
          age: cdpr.age.toString()
        }));

      const response = await api.post('/get-cdprs-pdf', selectedData, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'cdprs.pdf');
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

  const handleSelectCdpr = (code: string) => {
    setSelectedCdprs(prev => 
      prev.includes(code) 
        ? prev.filter(c => c !== code)
        : [...prev, code]
    );
  };

  const handleSelectAll = () => {
    if (selectedCdprs.length === filteredCdprs.length) {
      setSelectedCdprs([]);
    } else {
      setSelectedCdprs(filteredCdprs.map(cdpr => cdpr.code));
    }
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
            <h1 className="text-xl font-bold text-gray-800">Relatório de CDPR's</h1>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">
              {selectedCdprs.length} de {filteredCdprs.length} selecionados
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
                  placeholder="Buscar por código ou nome..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <button
                onClick={handlePrintReport}
                disabled={selectedCdprs.length === 0 || isGeneratingPDF}
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
                        checked={selectedCdprs.length === filteredCdprs.length && filteredCdprs.length > 0}
                        onChange={handleSelectAll}
                        className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </TableHead>
                    <TableHead className="font-semibold text-gray-700">Código</TableHead>
                    <TableHead className="font-semibold text-gray-700">Nome</TableHead>
                    <TableHead className="font-semibold text-gray-700">Faixa Etária</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCdprs.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-center py-8 text-gray-500">
                        Nenhum registro encontrado
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredCdprs.map((cdpr, index) => (
                      <TableRow 
                        key={index}
                        className="hover:bg-gray-50 transition-colors"
                      >
                        <TableCell className="text-center">
                          <input 
                            type="checkbox"
                            checked={selectedCdprs.includes(cdpr.code)}
                            onChange={() => handleSelectCdpr(cdpr.code)}
                            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </TableCell>
                        <TableCell className="font-medium text-gray-900">{cdpr.code}</TableCell>
                        <TableCell className="text-gray-700">{cdpr.name}</TableCell>
                        <TableCell className="text-gray-700">{cdpr.age}</TableCell>
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
