import {useState} from 'react'
import '../styles/dashboard.css'
import {NavBar} from "../components/NavBar.jsx"


export function Config({ setActivePage }){

    async function configUpdate(){
        let data = await fetch("http://localhost:8000/update-config", { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify(configObject) 
        })
    }

    const [configObject, setConfigObject] = useState({
        z_score: 0,
        min_moths: 3,
        isf_on: true,
        lof_on: true,
        pca_on: true
    })

    return (
    <>
        <NavBar setActivePage={setActivePage} />

        <form>
            <div className="panel">
                <h2>DETECTION THRESHOLDS</h2>
                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Provident Fund</h3>
                        <p>Maximum allowed deviation in PF contributions.</p>
                        <p>Records exceeding this percentage difference from expected are flagged</p>
                    </div>
                    <input type="number" onChange={(e) => setConfigObject({...configObject, z_score: e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>House Rent Allowance</h3>
                        <p>Maximum allowed deviation in HRA payments.</p>
                        <p>Flags records where HRA differs from expected by more than this percentage.</p>
                    </div>
                    <input type="number" onChange={(e) => setConfigObject({...configObject, min_months: e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Net Payable</h3>
                        <p>Maximum allowed deviation in final net salary.</p>
                        <p>The strictest threshold since net payable is the bottom line figure.</p>
                    </div>
                    <input type="number" onChange={(e) => setConfigObject({...configObject, min_months: e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Z-score threshold</h3>
                        <p>Flag records exceed this deviation</p>
                    </div>
                    <input type="number" onChange={(e) => setConfigObject({...configObject, z_score: e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Provident Fund Rate</h3>
                        <p>The standard Provident Fund contribution rate applied to basic salary.</p>
                        <p>Default is 12% (0.12) as per statutory requirement. Used as the baseline to calculate expected PF deductions.</p>
                    </div>
                    <input type="number" onChange={(e) => setConfigObject({...configObject, z_score: e.target.value})}></input>
                </div>

            </div>
                    

            <div className="panel">
                <h2>ML MODELS</h2>
                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Isolation forest</h3>
                        <p>Tree-based unsupervised anomaly detection</p>
                    </div>
                    <input type="checkbox" onChange={(e) => setConfigObject({...configObject, isf_on: e.target.value})}></input>
                </div>
                <hr />
                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Local outlier factor</h3>
                        <p>Density-based local anomaly scoring</p>
                    </div>
                    <input type="checkbox" onChange={(e) => setConfigObject({...configObject, lof_on: e.target.value})}></input>
                </div>
                <hr />
                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>PCA component analysis</h3>
                        <p>Reconstruction error anomaly detection</p>
                    </div>
                    <input type="checkbox" onChange={(e) => setConfigObject({...configObject, pca_on: e.target.value})}></input>
                </div>
            </div>

            <div className="run-download-buttons">
            <button>⎙ Save config</button>
            <button >Reset to defaults</button>
            </div>
        </form>

        </>
        )
}
