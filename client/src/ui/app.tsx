import OptionsComponent from "./components/options";

export default function App() {
  return (
    <>
      <p
        style={{
          width: "100vw",
          flex: 1,
          display: "flex",
          flexDirection: "column",
          gap: "2rem",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <OptionsComponent />
      </p>
    </>
  );
}
