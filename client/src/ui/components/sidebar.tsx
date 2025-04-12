import FileUploader from "@/components/file-uploader"

export default function Sidebar() {
  return (
    <div className="relative w-3/7 max-w-1/3 h-screen flex flex-col items-center justify-start border-r-2 border-[#DDD] p-6">
      <div className="flex justify-start items-center gap-1">
        <img src="/logo.png" alt="Logo" className="w-1/7 h-auto" />
        <p className="text-2xl font-semibold">Connect</p>
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
