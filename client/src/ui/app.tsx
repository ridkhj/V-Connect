
import Sidebar from "./components/sidebar";
import OptionsComponent from "./components/options";


export default function App() {
  return (
    <div className="w-screen h-screen flex overflow-hidden">
      <Sidebar />
      <div className="flex justify-center items-center w-full h-full bg-[#F1F1F1]">
        <OptionsComponent />
      </div>
    </div>
  );
}
