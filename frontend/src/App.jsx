import { LoginPage } from './pages/LoginPage.jsx'
import { Dashboard } from './pages/Dashboard.jsx'
// import { Prototype } from './pages/Prototype.jsx'
import { Config } from './pages/Config.jsx'
import { useState } from 'react'

export const defaultConfig = {
  pf_threshold: 0.1,
  hra_threshold: 0.05,
  net_payable: 0.01,
  z_score: 3.0,
  pf_rate: 0.12
}

export default function App(){
  
  const [configObject, setConfigObject] = useState(defaultConfig)
  
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activePage, setActivePage] = useState("dashboard")
  
  if (!isLoggedIn) {
     return <LoginPage onLogin={() => setIsLoggedIn(true)} />
   }

  if (activePage === "dashboard") return <Dashboard setActivePage={setActivePage} configObject={configObject} setConfigObject={setConfigObject} />
  // if (activePage === "analytics") return <Analytics setActivePage={setActivePage} />
  if (activePage === "config") return <Config setActivePage={setActivePage} configObject={configObject} setConfigObject={setConfigObject}/>
  


}

