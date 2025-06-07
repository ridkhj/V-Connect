import Sidebar from "./components/sidebar"
import Options from "./components/options"

export default function App() {
  return (
    <div className="w-screen h-screen flex overflow-x-hidden">
      <Sidebar />
      <div className="ml-[25%] w-full bg-zinc-50">
        <Options />
      </div>
    </div>
  )
}
