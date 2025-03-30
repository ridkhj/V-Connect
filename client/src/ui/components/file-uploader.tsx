import React, { useState, useRef, useCallback } from 'react';
import { File as FileIcon, MoreVertical, Upload } from 'lucide-react';
import { cn } from '../lib/utils';
import formatTimeAgo from '../functions/format-file-size';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  uploadedAt: Date;
}

const FileUploader = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedTab, setSelectedTab] = useState<'upload' | 'recent'>('upload');
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      addFiles(e.target.files);
    }
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

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + 'B';
    else if (bytes < 1048576) return Math.round(bytes / 1024) + 'KB';
    else return Math.round(bytes / 1048576) + 'MB';
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
    <div className="w-full bg-white rounded-lg shadow-sm border border-[#DDD]">
      <div className="flex p-4 gap-2 border-b-2 border-[#DDD]">
        <div className="w-full flex justify-center items-center">
          <div className="w-fit flex justify-center items-center p-1.5 rounded-full bg-[#F1F1F1]">
            <button
              onClick={() => setSelectedTab('upload')}
              className={cn(
                "py-1.5 px-4 rounded-full text-center font-medium text-sm transition-colors",
                selectedTab === 'upload' 
                  ? "bg-black text-white"
                  : "bg-transparent text-black" 
              )}
            >
              Fazer upload
            </button>
            <button
              onClick={() => setSelectedTab('recent')}
              className={cn(
                "py-1.5 px-4 rounded-full text-center font-medium text-sm transition-colors",
                selectedTab === 'recent' 
                  ? "bg-black text-white"
                  : "bg-transparent text-black" 
              )}
            >
              Recentes
            </button>
          </div>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
          multiple
        />
      </div>

      <div className="mt-4">
        {selectedTab === 'upload' ? (
          <div 
            className={cn(
              "p-8 border-2 border-dashed rounded-md mx-4 mb-4 transition-colors flex flex-col items-center justify-center",
              isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300"
            )}
            onDragEnter={handleDragEnter}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <Upload className="h-10 w-10 text-gray-400 mb-2" />
            <p className="text-center text-gray-500 mb-2">
              Arraste e solte arquivos aqui ou
            </p>
            <button 
              onClick={handleUploadClick}
              className="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              Escolha os arquivos
            </button>
          </div>
        ) : (
          files.length > 0 ? (
            <div>
              <div className="divide-y divide-gray-100">
                {files.slice(0, 4).map((file) => (
                  <div key={file.id} className="flex items-center justify-between px-4 py-3">
                    <div className="flex items-center gap-3">
                      <FileIcon className="h-5 w-5 text-gray-500" />
                      <div>
                        <p className="text-sm font-medium">{file.name}</p>
                        <p className="text-xs text-gray-500">{formatTimeAgo(file.uploadedAt)}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs bg-gray-50 py-1 px-2 rounded border border-gray-100">
                        {formatFileSize(file.size)}
                      </span>
                      <button className="text-gray-400 hover:text-gray-500">
                        <MoreVertical className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              
              {files.length > 4 && (
                <div className="p-4 flex justify-center">
                  <button 
                    className="text-sm font-medium text-gray-700 py-2 px-6 rounded-full border border-gray-200 hover:bg-gray-50 transition-colors"
                  >
                    Ver todos os uploads
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="p-8 text-center text-gray-500">
              <p>Nenhum arquivo carregado ainda</p>
              <button 
                onClick={handleUploadClick}
                className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-700"
              >
                Fazer upload
              </button>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default FileUploader;
