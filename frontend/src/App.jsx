import { LoginPage } from './pages/LoginPage.jsx'
import { Dashboard } from './pages/Dashboard.jsx'
// import { Prototype } from './pages/Prototype.jsx'
import { Config } from './pages/Config.jsx'
import { useState } from 'react'

export default function App(){
  
  
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activePage, setActivePage] = useState("dashboard")
  
  if (!isLoggedIn) {
     return <LoginPage onLogin={() => setIsLoggedIn(true)} />
   }

  if (activePage === "dashboard") return <Dashboard setActivePage={setActivePage} />
  // if (activePage === "analytics") return <Analytics setActivePage={setActivePage} />
  if (activePage === "config") return <Config setActivePage={setActivePage} />
  


}

