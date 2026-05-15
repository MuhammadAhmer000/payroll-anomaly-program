import {LogoBadge} from '../components/LogoBadge.jsx'
import '../styles/login.css'
import {useState} from 'react'
import {createClient} from '@supabase/supabase-js'

// 1. HOOKS
const url = import.meta.env.VITE_SUPABASE_URL
const key = import.meta.env.VITE_SUPABASE_KEY

const supabase = createClient(url, key)

export function LoginPage({onLogin }){
    
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    
    async function handleSubmit(e){
        console.log("submit clicked")
        e.preventDefault()

        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        })

        if (data.session) {
            onLogin()
        }

        if (error){
            alert(error.message)
            return
        }

        
    }
    // 2. HANDLERS
    
    // 3. JSX    
    
    return (
        <>
        
        <div className="page">

            <div className="header">
                <LogoBadge />
                <h2>Welcome back</h2>
                <p>Login in to your account</p>
            </div>

            <div className="card">

                <form  noValidate  onSubmit={handleSubmit}>
                    <label>Email</label>
                    <input autoComplete="off" type="email" onChange={(e) => setEmail(e.target.value)}/>
                    <label>Password</label>
                    <input type="password" onChange={(e) => setPassword(e.target.value)}/>
                    <button type="submit">Sign in</button>
                    
                </form>

            </div>
            

        </div>
        
        </>
    )


}