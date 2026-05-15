import { LoginPage } from './pages/LoginPage.jsx'
import { Dashboard } from './pages/Dashboard.jsx'
import { useState } from 'react'

export default function App(){
  
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  
  if (isLoggedIn) {
     return <Dashboard />
   }

   return <LoginPage onLogin={() => setIsLoggedIn(true)} />

}

