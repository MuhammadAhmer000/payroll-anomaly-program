import {useState} from 'react'
import {createClient} from '@supabase/supabase-js'

function DataTable({ title, data }) {
    if (!data || data.length === 0) return <p>{title}: No data</p>;
    const cols = Object.keys(data[0]);

    return (
        <div>
            <h3>{title}</h3>
            <table border="1" cellPadding="4">
                <thead>
                    <tr>{cols.map(c => <th key={c}>{c}</th>)}</tr>
                </thead>
                <tbody>
                    {data.map((row, i) => (
                        <tr key={i}>
                            {cols.map(c => <td key={c}>{String(row[c])}</td>)}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

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

    function handlePayrollUpload(e) {
        setPayrollFile(e.target.files[0])
    }

    async function uploadPayroll(){
        const formData = new FormData()
        formData.append("file", payrollFile)
        const response = await fetch("http://localhost:8000/upload", { method: "POST", body: formData })
        const data = await response.json()
        console.log(data)
    }

    function handleConfigUpload(e){
        setConfigFile(e.target.files[0])
    }

    async function uploadConfig(){
        const formData = new FormData()
        formData.append("file", configFile)
        const response = await fetch("http://localhost:8000/config", { method: "POST", body: formData })
        const data = await response.json()
        console.log(data)
    }

    async function runAnalysis() {
    try {
        const response = await fetch("http://localhost:8000/analyze", { method: "POST" })
        const text = await response.text()
        console.log("Raw response:", text)
        const data = JSON.parse(text)
        console.log("Parsed data:", data)
        setResult(Array.isArray(data) ? data : [])
    } catch (err) {
        console.error("Fetch failed:", err)
    }
}

    async function authenticate(event){
        event.preventDefault();
        let {data, error} = await supabase.auth.signInWithPassword({email, password})
        console.log(data);
        console.log(error);
        if (error){
            alert("ERROR: COULD NOT RETRIEVE USER")
        } else {
            setIsLoggedIn(true)
        }
    }

    if (!isLoggedIn){
        return (
            <>
            <form onSubmit={authenticate}>
                Username: <input name="username" onChange={(e) => setUsername(e.target.value)} /><br/>
                Email: <input name="email" onChange={(e) => setEmail(e.target.value)} /><br/>
                Password: <input name="password" onChange={(e) => setPassword(e.target.value)} /><br/>
                <button>Submit</button>
            </form>
            </>
        );
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <pre style={{background: '#eee', padding: 8, fontSize: 12}}>
            {JSON.stringify(result, null, 2)}
            </pre>
            <button onClick={uploadPayroll}>Upload Payroll File</button>
            <input type="file" onChange={handlePayrollUpload} />
            <button onClick={uploadConfig}>Upload Config File</button>
            <input type="file" onChange={handleConfigUpload} />
            <button onClick={runAnalysis}>Run Analysis</button>

            {result && result.map(emp => (
                <div key={emp.emp_id}>
                    <h2>Employee {emp.emp_id}</h2>
                    <DataTable title="Rules" data={emp.rule_df} />
                    <DataTable title="Stats" data={emp.stats_df} />
                    <DataTable title="Unsupervised" data={emp.unsupervised_df} />
                    <DataTable title="Ensemble" data={emp.ensemble_df} />
                    <DataTable title="Root Cause" data={emp.root_cause_df} />
                    <DataTable title="Root Cause Summary" data={emp.root_cause_summary} />
                </div>
            ))}
        </div>
    )
}