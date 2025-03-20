import { app, BrowserWindow } from "electron"
import path from "path"
import { isDev } from "./utils/isDev.js"

app.on("ready", () => {
    const mainWindow = new BrowserWindow({
        icon: "logo.png",
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })
    
    if (isDev()) {
        mainWindow.loadURL("http://localhost:5132")
    } else {
        mainWindow.loadFile(path.join(app.getAppPath(), "/dist-react/index.html"))
    }
})