import { ArrowLeft } from "lucide-react"
import Sidebar from "../../components/sidebar"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@//components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@//components/ui/select" 

const peoples = [
  {
    code: "12616",
    participant_code: "f2348f15a-3f1jf",
    name: "Edson Alves da Silva",
    type: "Autista",
    state: "PB"
  },
  {
    code: "12616",
    participant_code: "f2348f15a-3f1jf",
    name: "Wedne Morais de Araújo",
    type: "Macaco",
    state: "PB"
  }
]

export default function Cards() {
  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="w-full bg-zinc-50">
        <header className="flex justify-start items-center gap-4 p-4 bg-white border-b-2 border-[#DDD]">
          <button>
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-xl font-bold uppercase">Relatório de Cartas</h1>
        </header>
        <div className="flex justify-end items-center gap-2 mx-12 mt-12">
          <button className="bg-[#8270fa] text-white rounded-md py-1 px-4 flex items-center font-semibold">
            <p>Imprimir Relatório</p>
          </button>
          <button className="bg-[#8270fa] text-white rounded-md py-1 px-4 flex items-center font-semibold">
            <p>Enviar Email</p>
          </button> 
        </div>
        <div className="mx-12">
          <Table className="my-2 border-2 border-[#DDD]">
            <TableHeader className="bg-zinc-100 border-1 border-[#DDD]">
              <TableRow>
                <TableHead className="text-center border-r-1 border-[#DDD]">
                  <input type="checkbox" />
                </TableHead>
                <TableHead className="font-bold border-r-1 border-[#DDD]">Código</TableHead>
                <TableHead className="font-bold border-r-1 border-[#DDD]">Código do participante</TableHead>
                <TableHead className="font-bold border-r-1 border-[#DDD]">Nome</TableHead>
                <TableHead className="font-bold border-r-1 border-[#DDD]">Tipo</TableHead>
                <TableHead className="font-bold border-r-1 border-[#DDD]">Estado</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {peoples.map((people, index) => (
                <TableRow key={index}>
                  <TableCell className="text-center border-r-1 border-[#DDD]">
                    <input type="checkbox" />
                  </TableCell>
                  <TableCell className="font-medium border-r-1 border-[#DDD]">{people.code}</TableCell>
                  <TableCell className="font-medium border-r-1 border-[#DDD]">{people.participant_code}</TableCell>
                  <TableCell className="font-medium border-r-1 border-[#DDD]">{people.name}</TableCell>
                  <TableCell className="border-r-1 border-[#DDD] px-4">
                    <Select defaultValue="Autista">
                      <SelectTrigger className="border-1 pl-2 pr-1 border-[#DDD] rounded-sm h-8 w-full">
                        <SelectValue placeholder="Selecione o tipo" />
                      </SelectTrigger>
                      <SelectContent className="border-1 border-[#DDD] rounded-md">
                        <SelectItem value="Autista">Autista</SelectItem>
                        <SelectItem value="Macaco">Macaco</SelectItem>
                      </SelectContent>
                    </Select>
                  </TableCell>
                  <TableCell>{people.state}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
