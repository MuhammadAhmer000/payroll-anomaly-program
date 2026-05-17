import { LoginPage } from './pages/LoginPage.jsx'
import { Dashboard } from './pages/Dashboard.jsx'
import { Prototype } from './pages/Prototype.jsx'
import { useState } from 'react'

export default function App(){
  
  return <Prototype />
  /*
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  
  if (isLoggedIn) {
     return <Dashboard />
   }

   return <LoginPage onLogin={() => setIsLoggedIn(true)} />
  */


}

