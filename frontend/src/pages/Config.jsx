import {useState} from 'react'
import '../styles/dashboard.css'
import { defaultConfig } from "../App.jsx"
import {NavBar} from "../components/NavBar.jsx"


export function Config({ setActivePage, configObject, setConfigObject }){

    console.log("CONFIG OBJECT:", configObject)

    async function configUpdate(e){
        
        e.preventDefault();

        let data = await fetch("http://localhost:8000/update-config", { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify(configObject) 
        })

        console.log(configObject)
    }

    return (
    <>
        <NavBar setActivePage={setActivePage} />

        <form noValidate onSubmit={configUpdate}>
            <div className="panel">
                <h2>DETECTION THRESHOLDS</h2>
                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Provident Fund</h3>
                        <p>Maximum allowed deviation in PF contributions.</p>
                        <p>Records exceeding this percentage difference from expected are flagged</p>
                    </div>
                    <input type="number" value={configObject.pf_threshold} onChange={(e) => setConfigObject({...configObject, pf_threshold: +e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>House Rent Allowance</h3>
                        <p>Maximum allowed deviation in HRA payments.</p>
                        <p>Flags records where HRA differs from expected by more than this percentage.</p>
                    </div>
                    <input type="number" value={configObject.hra_threshold} onChange={(e) => setConfigObject({...configObject, hra_threshold: +e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Net Payable</h3>
                        <p>Maximum allowed deviation in final net salary.</p>
                        <p>The strictest threshold since net payable is the bottom line figure.</p>
                    </div>
                    <input type="number" value={configObject.net_payable} onChange={(e) => setConfigObject({...configObject, net_payable: +e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Z-score threshold</h3>
                        <p>Flag records exceed this deviation</p>
                    </div>
                    <input type="number" value={configObject.z_score} onChange={(e) => setConfigObject({...configObject, z_score: +e.target.value})}></input>
                </div>

                <hr />

                <div className="config-panel-header">
                    <div className="config-subpanel-header">
                        
                        <h3>Provident Fund Rate</h3>
                        <p>The standard Provident Fund contribution rate applied to basic salary.</p>
                        <p>Default is 12% (0.12) as per statutory requirement. Used as the baseline to calculate expected PF deductions.</p>
                    </div>
                    <input type="number" value={configObject.pf_rate} onChange={(e) => setConfigObject({...configObject, pf_rate: +e.target.value})}></input>
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
            <button type="submit">⎙ Save config</button>
            <button onClick={() => setConfigObject({...defaultConfig})}>Reset to defaults</button>
            </div>
        </form>

        </>
        )
}
