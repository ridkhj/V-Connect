import Sidebar from "@/components/sidebar"
import { Link } from "react-router-dom"
import { ArrowLeft, Copy } from "lucide-react"
import {
  Table,
  TableHeader,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@/components/ui/table"

const peoples = [
  {
    code: "12616",
    participant_code: "f2348f15a-3f1jf",
    name: "Edson Alves da Silva",
    type: "Tipozinho",
    state: "PB",
  },
  {
    code: "12616",
    participant_code: "f2348f15a-3f1jf",
    name: "Wedne Morais de Araújo",
    type: "Tipozão",
    state: "PB",
  },
];

export default function Updates() {
  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="w-full bg-zinc-50">
        <header className="flex justify-start items-center gap-4 p-4 bg-white border-b-2 border-[#DDD]">
          <Link to="/">
            <ArrowLeft size={24} />
          </Link>
          <h1 className="text-xl font-bold uppercase">
            Relatório de Atualizações
          </h1>
        </header>
        <div className="flex justify-end items-center gap-2 mx-12 mt-12">
          <button className="bg-indigo-600 text-white rounded-full py-2 px-4 text-sm flex items-center font-semibold">
            <p>Imprimir formuários</p>
          </button>
          <button className="bg-indigo-600 text-white rounded-full py-2 px-4 text-sm flex items-center font-semibold">
            <p>Google Forms</p>
          </button>
        </div>
        <div className="mx-12">
          <Table className="my-4 border-2 border-[#DDD]">
            <TableHeader className="bg-zinc-100 border-1 border-[#DDD]">
              <TableRow>
                <TableHead className="font-black border-r-1 border-[#DDD] w-[50%]">
                  Nome
                </TableHead>
                <TableHead className="font-black border-r-1 border-[#DDD]">
                  Código
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {peoples.map((people, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium border-r-1 border-[#DDD]">
                    {people.name}
                  </TableCell>
                  <TableCell className="font-medium border-r-1 border-[#DDD]">
                    {people.code}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
      <button className="fixed bottom-8 right-8 bg-indigo-600 text-white rounded-full p-4 flex items-center font-semibold">
        <Copy />
      </button>
    </div>
  );
}
