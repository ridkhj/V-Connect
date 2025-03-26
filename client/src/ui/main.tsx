import './index.css'

import '@aws-amplify/ui-react/styles.css'
import '@aws-amplify/ui-react/styles/reset.layer.css'
import '@aws-amplify/ui-react/styles/base.layer.css'
import '@aws-amplify/ui-react/styles/button.layer.css'

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './app'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
