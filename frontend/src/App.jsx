import {useState} from 'react'
import {createClient} from '@supabase/supabase-js'


export default function App(){
  const [payrollFile, setPayrollFile] = useState(null)
  const [configFile, setConfigFile] = useState(null)
  const [result, setResult] = useState(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const URL = "https://fkhvhuclngjvnyrojqvd.supabase.co"
  const KEY = "sb_publishable_ed6psE3oqTkIMt0yqy6P_Q_ArXdfv0E"
  const supabase = createClient(URL, KEY);

  // file input
  function handlePayrollUpload(e) {
    setPayrollFile(e.target.files[0])
  }

  async function uploadPayroll(){
    const formData = new FormData()
    formData.append("file", payrollFile)
    const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData

    })

    const data = await response.json()
    console.log(data)
  }

  // config
  function handleConfigUpload(e){
    setConfigFile(e.target.files[0])
  }

  async function uploadConfig(){
    const formData = new FormData()
    formData.append("file", configFile)
    const response = await fetch("http://localhost:8000/config", {
        method: "POST",
        body: formData

    })

    const data = await response.json()
    console.log(data)
  }

  // analyze
  async function runAnalysis() {
    const response = await fetch("http://localhost:8000/analyze", {
        method: "POST"
    })
    const data = await response.json()
    setResult(data)
  }

  async function authenticate(event){
    event.preventDefault();
    let {data, error} = await supabase.auth.signInWithPassword({email, password})
    console.log(data);
    console.log(error);

    if (error){
    alert("ERROR: COULD NOT RETRIEVE USER")
    } else{
        setIsLoggedIn(true)
    }



  }


  if (!isLoggedIn){
      return (
        <>
        <form onSubmit={authenticate}>
        Username: <input name="username" onChange={(e) => {setUsername(e.target.value);console.log(e.target.value)}}></input><br></br>
        Email: <input name="email" onChange={(e) => {setEmail(e.target.value);console.log(e.target.value)}}></input><br></br>
        Password: <input name="password" onChange={(e) => {setPassword(e.target.value);console.log(e.target.value)}}></input><br></br>
        <button>Submit</button>
        </form>
        </>

      );
  }

  return (
    <div>
        <h1>Dashboard</h1>
        <button onClick={uploadPayroll}>Upload Payroll File</button>
        <input type="file" onChange={handlePayrollUpload} />
        <button onClick={uploadConfig}>Upload Config File</button>
        <input type="file" onChange={handleConfigUpload} />
        <button onClick={runAnalysis}>Run Analysis</button>
        {result && <p>{result.message}</p>}
    </div>

  )

}