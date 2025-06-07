import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Letters from "./pages/letters"
import Cdprs from "./pages/cdprs"
import Updates from "./pages/updates"

import "./index.css"
import App from "./app"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App/>} />
        <Route path="/letters" element={<Letters />} />
        <Route path="/updates" element={<Updates />} />
        <Route path="/cdprs" element={<Cdprs/>} />
      </Routes>
    </Router>
  </StrictMode>
)
