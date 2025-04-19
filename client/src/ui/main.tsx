import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"

import App from "@/app"
import Cards from "@/pages/cards"
import Cdprs from "@/pages/cdprs"
import Updates from "@/pages/updates"

import "@/index.css"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/cards" element={<Cards />} />
        <Route path="/updates" element={<Updates />} />
        <Route path="/cdprs" element={<Cdprs/>} />
      </Routes>
    </Router>
  </StrictMode>
)
