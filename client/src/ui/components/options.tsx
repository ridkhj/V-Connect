import { Link } from "react-router-dom"
import { ChevronRight, FileText, Mail, Upload } from "lucide-react"

export default function Options() {
  const options = [
    {
      title: "Relatório de Atualizações",
      path: "/updates",
      icon: <Upload size={24} />,
      status: "45 vencidas",
      color: "from-violet-500 to-violet-600"
    },
    {
      title: "Relatório de CDPR'S",
      path: "/cdprs",
      icon: <FileText size={24} />,
      status: "7 vencidas, 4 a fazer",
      color: "from-indigo-500 to-indigo-600"
    },
    {
      title: "Relatório de Cartas",
      path: "/letters",
      icon: <Mail size={24} />,
      status: "7 vencidas, 4 a fazer",
      color: "from-blue-500 to-blue-600"
    }
  ]

  return (
    <main className="w-full h-full px-36 flex justify-center items-center flex-col gap-4">
      {options.map((option) => (
        <Link
          key={option.path}
          to={option.path}
          className={`w-full p-6 rounded-lg bg-gradient-to-r ${option.color} 
            hover:shadow-lg transition-all duration-200 group relative overflow-hidden`}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-white/25 rounded-lg text-white">
                {option.icon}
              </div>
              <div>
                <h1 className="text-white font-bold text-2xl">
                  {option.title}
                </h1>
                <p className="text-white/80 font-medium">
                  {option.status}
                </p>
              </div>
            </div>
            <div className="opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="bg-white/25 rounded-full p-2">
                <ChevronRight size={24} className="text-white"/>
              </div>
            </div>
          </div>
        </Link>
      ))}
    </main>
  )
}
