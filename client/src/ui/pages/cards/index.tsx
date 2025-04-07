import Sidebar from "@//components/sidebar";
import "./style.css";
import { ArrowLeft } from "lucide-react";

export default function Cards() {
  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="container">
        <header className="header1">
          <ArrowLeft className="seta" />
          <h1>Relatório de Cartas</h1>
        </header>
        <div className="botoes">
          <button className="botao1">
            <p>Imprimir Relatório</p>
          </button>
          <button className="botao2">
            <p>Enviar Email</p>
          </button>
        </div>
        <div className="table"></div>
      </div>
    </div>
  );
}
