import Sidebar from "@/components/sidebar"
import Options from "@/components/options"
import { useEffect } from "react"
import { api } from "./constants/api"

export default function App() {
  useEffect(() => {
    async function sendRequest() {
      try {
        const res = await api.post("/send-email", {
          recipients: "devedsonalves@gmail.com",
          subject: "V Connect",
          body: "Olá! Este é um e-mail enviado do frontend para test"
        });
        console.log(res.data);
      } catch (err) {
        console.log('Deu erro: ' + err);
      }
    }

    sendRequest()
}, [])

  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="w-full bg-zinc-50">
        <Options />
      </div>
    </div>
  )
}
