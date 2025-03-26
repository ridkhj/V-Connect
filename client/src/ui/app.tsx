import DropzoneComponent from "./components/dropzone"

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
          alignItems: "center" 
       }}>
        <DropzoneComponent />
      </p>
    </>
  )
}