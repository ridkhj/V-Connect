import {
  useState,
  useRef,
  ChangeEvent
} from 'react'

import {
  Button,
  DropZone,
  Flex,
  Text,
  VisuallyHidden,
} from '@aws-amplify/ui-react'

const acceptedFileTypes: string[] = ['.csv'];

interface CsvFile extends File {
  name: string;
}

export default function DropzoneComponent() {
  const [uploadedFiles, setUploadedFiles] = useState<CsvFile[]>([])
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  const handleFileSelection = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const { files } = event.target
    const hasNoFiles = !files || files.length === 0

    if (hasNoFiles) {
      return
    }

    const newFiles = Array.from(files) as CsvFile[]
    setUploadedFiles((prevFiles) => [...prevFiles, ...newFiles])
  };

  return (
    <>
      <DropZone
        acceptedFileTypes={acceptedFileTypes}
        onDropComplete={({ acceptedFiles }) => {
          const newFiles = acceptedFiles
          setUploadedFiles((prevFiles) => [...prevFiles, ...newFiles])
        }}
      >
        <Flex direction="column" alignItems="center">
          <Text>Arraste o arquivo .csv ou</Text>
          <Button size="small" onClick={() => fileInputRef.current?.click() }>
            Selecione o arquivo
          </Button>
        </Flex>
        <VisuallyHidden>
          <input
            type="file"
            tabIndex={-1}
            ref={fileInputRef}
            onChange={handleFileSelection}
            multiple
            accept={acceptedFileTypes.join(',')}
          />
        </VisuallyHidden>
      </DropZone>

      {uploadedFiles.length > 0 && (
        <div>
          <Text>Arquivos Recebidos</Text>
          {uploadedFiles.map((file) => (
            <Text key={file.name}>{file.name}</Text>
          ))}
        </div>
      )}
    </>
  );
}
