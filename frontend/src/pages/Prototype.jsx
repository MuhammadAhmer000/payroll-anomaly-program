import '../styles/prototype.css'
import { LogoBadge } from '../components/LogoBadge.jsx'
import {useState} from 'react'



function RulesTable({data}){

  const rows = []
  for (let row of data){
    rows.push(
      <tr key={row.Name}>
        <td>{row.Name}</td>
        <td>{row.Actual}</td>
        <td>{row.Expected}</td>
        <td>
          <span className={row.Anomaly ? "badge-anomaly" : "badge-clean"}>
          {row.Anomaly ? "Yes" : "No"}
          </span>
        </td>
        
      </tr>

    )
  } 

  return(
    <table className="rules-table">
      <thead>
        <tr>
          <th>NAME</th>
          <th>ACTUAL</th>
          <th>EXPECTED</th>
          <th>ANOMALY</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>




  )
}

function MLTable({data}){
   const rows = []
  for (let row of data){
    rows.push(
      <tr key={row.IF_Anomaly}>
        <td>{row.IF_Anomaly ? "Yes" : "No"}</td>
        <td>{row.LOF_Anomaly ? "Yes" : "No"}</td>
        <td>{row.PCA_Anomaly ? "Yes" : "No"}</td>
        <td>
          <span className={row.Ensemble_Anomaly ? "badge-anomaly" : "badge-clean"}>
          {row.Ensemble_Anomaly ? "Yes" : "No"}
          </span>
        </td>
        
      </tr>

    )
  } 

  return(
    <table className="rules-table">
      <thead>
        <tr>
          <th>ISOLATION FOREST</th>
          <th>LOCAL OUTLIER FACTOR</th>
          <th>COMPONENT ANALYSIS</th>
          <th>ANOMALY</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>




  )
}

function StatsTable({data}){
   const rows = []
  for (let row of data){
    rows.push(
      <tr key={row.field}>
        <td>{row.field}</td>
        <td>{row.z_score > 0 ? "+" + row.z_score.toFixed(2) : row.z_score.toFixed(6)}</td>
        <td>{row.z_score_deviation.toFixed(1)}</td>
        <td>
          <span className={row.anomaly ? "badge-anomaly" : "badge-clean"}>
          {row.anomaly ? "Yes" : "No"}
          </span>
        </td>
        
      </tr>

    )
  } 

  return(
    <table className="rules-table">
      <thead>
        <tr>
          <th>FIELD</th>
          <th>Z-SCORE</th>
          <th>Z-SCORE DEVIATION</th>
          <th>ANOMALY</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>




  )
}


function EmployeeCard({data}){

  return (
    <>
    
      <div className="employee-card"> 
            <div className="employee-card-header">
              <h2>Employee {data.emp_id}</h2>
              <span 
                className={data.overall ? "badge-anomaly" : "badge-clean"}>
                {data.overall ? "Anomaly" : "Not Anomaly"}
              </span>
            </div>
            <hr />
            <p>RULES</p>
              <RulesTable data={data.rule_df} />
            <p>MACHINE LEARNING</p>
              <MLTable data={data.ensemble_df} />
            <p>STATISTICAL SUMMARY</p>
              <StatsTable data={data.stats_df} />
      </div>
    
    
    </>
  )

}


function NEmployees({data}){
  const cards = []
  for (let employee of data){
    cards.push(
      <EmployeeCard key={employee.emp_id} data={employee} />
    )
  }

  return cards
}





// change the file upload later to change on :hover // 
export function Prototype(){

  const [payrollFile, setPayrollFile] = useState(null)
  const [config, setConfig] = useState(null)
  const [output, setOutput] = useState(null)
  const [inputMethod, setInputMethod] = useState("excel") // "excel" or "db"
  const [dbCredentials, setDbCredentials] = useState({
    host: "",
    port: "",
    database: "",
    username: "",
    password: ""
  })
  
  async function uploadPayroll(){
  const formData = new FormData()
  formData.append("file", payrollFile)

  let data = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData
  })

  return data
  }


  async function uploadConfig(){
    const formData = new FormData()
    formData.append("file", config)

    let data = await fetch("http://localhost:8000/config", {
      method: "POST",
      body: formData
    })

    return data
  }

  async function uploadDBPayroll(){

    let data = await fetch("http://localhost:8000/upload-db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dbCredentials)
    })

    return data
  }



  async function runAnalysis(){

    if (inputMethod == "excel"){
       if (config == null || payrollFile == null){
       alert("FILE MISSING: CHECK PAYROLL & CONFIG")
       return
       }

      await uploadConfig()
      await uploadPayroll()

    } else if (inputMethod == "db"){
        await uploadConfig()
        await uploadDBPayroll()
    }

      const data = await fetch("http://localhost:8000/analyze", {
        method: "POST"
      })


      const results = await data.json()
      setOutput(results)
  }

  async function download(){

    let data = await fetch("http://localhost:8000/download", {
        method: "POST",
    })

    const blob = await data.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "results.xlsx"
    a.click()
    URL.revokeObjectURL(url)

  }


  function Data_Input(){

    if (inputMethod == "excel"){  // fix this
        return(
            <>
                <div className="upload-inputs">
                    <div className="upload-field">
                        <label>Payroll file</label>

                        <label className={payrollFile ? "upload-file upload-file--ready" : "upload-file"}>
                            <span>Choose file → Upload</span>   
                            <input type="file" onChange={(e) => setPayrollFile(e.target.files[0])} hidden />
                        </label>

                    </div>
                    <div className="upload-field">
                        <label>Config file</label>

                        <label className={config ? "upload-file upload-file--ready" : "upload-file"}>
                            <span>Choose file → Upload</span>   
                            <input type="file" onChange={(e) => setConfig(e.target.files[0])} hidden />
                        </label>
                    </div>
                </div>
            </>
        )
    }
    else if (inputMethod == "db"){   // fix this
        return(
            <>
                <div className="upload-inputs">
                    <div className="upload-field">
                        <label>Host</label>
                        <label>
                            <input type="text" onChange={(e) => setDbCredentials({...dbCredentials, host: e.target.value})}/>
                        </label>
                    </div>
                    <div className="upload-field">
                        <label>Port</label>
                        <label>
                            <input type="text" onChange={(e) => setDbCredentials({...dbCredentials, port: e.target.value})}/>
                        </label>
                    </div>
                </div>
                <div className="upload-inputs">
                    <div className="upload-field">
                        <label>Database</label>
                        <label>
                            <input type="text" onChange={(e) => setDbCredentials({...dbCredentials, database: e.target.value})}/>
                        </label>
                    </div>
                    <div className="upload-field">
                        <label>Username</label>
                        <label>
                            <input type="text" onChange={(e) => setDbCredentials({...dbCredentials, username: e.target.value})}/>
                        </label>
                    </div>
                </div>
                <div className="upload-inputs">
                    <div className="upload-field">
                        <label>Password</label>
                        <label>
                            <input type="password" onChange={(e) => setDbCredentials({...dbCredentials, password: e.target.value})}/>
                        </label>
                    </div>
                </div>
            </>
        )
    }
    }

    return (<>
        <div className="dash-header">
        <h2>Machine Learning Payroll Anomaly Detection System</h2>
        <div className="options">
            <button>Analysis</button>
            <button>Analytics</button>
            <button>Config</button>
        </div>
        </div>
        <hr />
        <div className="panel">
            <div className="panel-header">
                <h2>DATA INPUT</h2>
                <div className="panel-header-buttons">
                    <button className="excel-button" onClick={() => setInputMethod("excel")}>Excel</button>
                    <button className="db-button" onClick={() => setInputMethod("db")}>Database</button>
                </div>
            </div>
            {Data_Input()}

            <button onClick={runAnalysis}>Run analysis</button>
            <button onClick={download} disabled={output === null}>Download</button>


        </div>


        {output && <NEmployees data={output} />}
        


      
    
    </>)
}