import FileUploader from "@/components/file-uploader"

export default function Sidebar() {
  return (
    <div className="fixed w-1/4 h-screen flex flex-col items-center justify-start bg-white border-r-2 border-[#DDD] p-6">
      <div className="w-full flex justify-start items-center gap-4 py-4">
        <div className="flex items-center justify-start gap-4">
          <div className="bg-zinc-100 p-2 rounded-lg">
            <img src="/logo.png" alt="Logo" className="w-10 h-10" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">V Connect</h1>
            <p className="text-xs text-gray-500">Gerenciamento de Documentos</p>
          </div>
        </div>
      </div>

      <div className="mt-5 w-full">
        <FileUploader />
      </div>

      <div className="bg-white absolute bottom-0 left-0 w-full border-t-2 border-#ddd p-2 flex justify-center items-center">
        <p className="text-xs font-medium">
          © 2025 V Connect | Todos os direitos reservados.
        </p>
      </div>
    </div>
  )
}
