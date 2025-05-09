import { Link } from "react-router-dom"

export default function Options() {
  return (
    <main className="w-full h-full px-36 flex justify-center items-center flex-col gap-4">
      <Link to="/updates" className="w-full bg-indigo-600 rounded-lg border-r-24 border-cyan-300 p-6">
        <h1 className="text-white text-left flex font-bold text-2xl">
          Relatório de Atualizações
        </h1>
        <p className="text-zinc-300 font-medium flex text-lg">45 vencidas</p>
      </Link>
      <Link to="/cdprs" className="w-full bg-indigo-600 rounded-lg border-r-24 border-cyan-300 p-6">
        <h1 className="text-white text-left flex font-bold text-2xl">
          Relatório de CDPR´S
        </h1>
        <p className="text-zinc-300 font-medium flex text-lg">
          7 vencidas, 4 a fazer
        </p>
      </Link>
      <Link to="/cards" className="w-full bg-indigo-600 rounded-lg border-r-24 border-cyan-300 p-6">
        <h1 className="text-white text-left flex font-bold text-2xl">
          Relatório de Cartas
        </h1>
        <p className="text-zinc-300 font-medium flex text-lg">
          7 vencidas, 4 a fazer
        </p>
      </Link>
    </main>
  )
}
