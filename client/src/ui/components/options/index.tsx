import "./styles.css";

export default function OptionsComponent() {
  return (
    <main>
      <button className="botao">
        <h1 className="titulo">Relatório de Atualizações</h1>
        <p className="notificacao">45 vencidas</p>
      </button>
      <button className="botao">
        <h1 className="titulo">Relatório de CDPR´S</h1>
        <p className="notificacao">7 vencidas, 4 a fazer</p>
      </button>
      <button className="botao">
        <h1 className="titulo">Relatório de Cartas</h1>
        <p className="notificacao">7 vencidas, 4 a fazer</p>
      </button>
    </main>
  );
}
