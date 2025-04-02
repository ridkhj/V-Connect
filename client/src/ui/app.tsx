import Options from "./components/options";
import Sidebar from "./components/sidebar";

export default function App() {
  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="flex justify-center items-center w-full h-full bg-[#F1F1F1]">
        <Options />
      </div>
    </div>
  );
}
