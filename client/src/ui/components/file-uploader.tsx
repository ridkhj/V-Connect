import React, { useState, useRef, useCallback } from 'react'
import { CheckCircle2, FileIcon, Trash, Upload } from 'lucide-react'
import { cn } from '../lib/utils'
import formatTimeAgo from '../functions/format-time-ago'
import { Card, CardContent } from './ui/card'
import { Progress } from './ui/progress'
import { formatFileSize } from '../functions/format-size-file'

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  uploadedAt: Date;
}

interface FileUploaderProps {
  onUpload: (file: File) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onUpload }) => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedTab, setSelectedTab] = useState<'upload' | 'recent'>('upload');
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      uploadFiles(e.target.files);
      onUpload(e.target.files[0]);
    }
  };

  const uploadFiles = (fileList: FileList) => {
    setUploading(true);
    setUploadProgress(0);
    
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 5;
      });
    }, 100);
    
    setTimeout(() => {
      clearInterval(interval);
      setUploadProgress(100);
      
      const newFiles = Array.from(fileList).map(file => ({
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        size: file.size,
        uploadedAt: new Date()
      }));
      
      setFiles(prev => [...newFiles, ...prev]);
      
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    
      setTimeout(() => {
        setUploading(false);
        setUploadProgress(0);
      }, 500);
    }, 2000);
  };

  const deleteFile = (id: string) => {
    setFiles((prevFiles) => prevFiles.filter((file) => file.id !== id));
  };

  const addFiles = (fileList: FileList) => {
    const newFiles = Array.from(fileList).map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      uploadedAt: new Date()
    }));
    
    setFiles(prev => [...newFiles, ...prev]);
    
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleDragEnter = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      addFiles(e.dataTransfer.files);
    }
  }, []);

  return (
    <Card className="w-full p-0 max-w-md bg-white shadow-md overflow-hidden border-2 border-[#DDD]">
      <div className="flex p-4 gap-1.5 border-b-2 border-[#DDD]">
        <button
          onClick={() => setSelectedTab('upload')}
          className={cn(
            "flex-1 py-2 px-4 rounded-full text-center font-bold text-sm transition-colors",
            selectedTab === 'upload' 
              ? "bg-indigo-600 text-white hover:bg-indigo-700"
              : "bg-[#f1f1f1] text-indigo-600" 
          )}
        >
          Fazer upload
        </button>
        <button
          onClick={() => setSelectedTab('recent')}
          className={cn(
            "flex-1 py-2 px-4 rounded-full text-center font-bold text-sm transition-colors",
            selectedTab === 'recent' 
              ? "bg-indigo-600 text-white hover:bg-indigo-700"
              : "bg-[#f1f1f1] text-indigo-600" 
          )}
        >
          Recentes
        </button>
        <input
          id='file-input'
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
          multiple
        />
      </div>

      <CardContent className="p-0">
        {selectedTab === 'upload' ? (
          <>
            <div 
              className={cn(
                "p-8 m-4 mt-0 border-2 border-dashed rounded-lg transition-colors flex flex-col items-center justify-center",
                isDragging 
                  ? "border-indigo-400 bg-indigo-50" 
                  : "border-gray-300 hover:border-indigo-300 hover:bg-gray-50"
              )}
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {uploading ? (
                <div className="text-center space-y-3">
                  <div className="bg-indigo-50 p-4 rounded-full inline-flex items-center justify-center mb-2">
                    <Upload className="h-8 w-8 text-indigo-500" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-700">
                    Enviando arquivos...
                  </h3>
                </div>
              ) : (
                <div className="text-center space-y-3">
                  <div className="bg-indigo-50 p-4 rounded-full inline-flex items-center justify-center mb-2">
                    <Upload className="h-8 w-8 text-indigo-500" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-700">
                    Arraste e solte seus arquivos
                  </h3>
                  <p className="text-center text-gray-500 text-sm max-w-xs">
                    ou
                  </p>
                  <button 
                    onClick={handleUploadClick}
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-700 bg-white border border-indigo-300 rounded-full px-4 py-2 hover:bg-indigo-50 transition-colors"
                  >
                    Escolha os arquivos
                  </button>
                </div>
              )}
            </div>
            
            {uploading && (
              <div className="px-6 pb-6 space-y-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    Progresso do upload
                  </span>
                  <span className="text-sm font-medium text-indigo-600">
                    {uploadProgress}%
                  </span>
                </div>
                <Progress
                  value={uploadProgress}
                  className="h-2 w-full bg-gray-100"
                />
                <div className="flex items-center justify-center mt-2">
                  {uploadProgress === 100 && (
                    <div className="flex items-center text-green-500 gap-1 text-sm">
                      <CheckCircle2 className="h-4 w-4" />
                      <span>Upload 
                        concluído!</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="py-2">
            {files.length > 0 ? (
              <>
                <div className="divide-y divide-gray-100">
                  {files.slice(0, 4).map((file) => (
                    <div key={file.id} className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="bg-indigo-50 p-2 rounded">
                          <FileIcon className="h-5 w-5 text-indigo-500" />
                        </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700">
                              {file.name.length > 15 ? file.name.slice(0, 15) + '...' : file.name}
                            </p>
                          <p className="text-xs text-gray-500">{formatTimeAgo(file.uploadedAt)}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs bg-gray-100 py-1 px-2 rounded-full text-gray-600 font-medium">
                          {formatFileSize(file.size)}
                        </span>
                        <button className="text-red-400 hover:text-red-600 p-1 rounded-full hover:bg-gray-100">
                          <Trash onClick={() => deleteFile(file.id)} className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                
                {files.length > 4 && (
                  <div className="p-4 flex justify-center">
                    <button 
                      className="text-sm font-medium text-indigo-600 py-2 px-6 rounded-full border border-indigo-200 hover:bg-indigo-50 transition-colors"
                    >
                      Ver todos os uploads
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="p-10 pt-4 text-center">
                <div className="bg-gray-50 p-4 rounded-full inline-flex items-center justify-center mb-2">
                  <FileIcon className="h-6 w-6 text-gray-400" />
                </div>
                <p className="text-gray-500">Nenhum arquivo carregado ainda</p>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUploader;
