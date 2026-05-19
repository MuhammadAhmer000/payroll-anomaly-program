import {useState} from 'react'
import '../styles/dashboard.css'


export function Config(){
    return (
    <>
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
            <h2>DETECTION THRESHOLDS</h2>
            <div className="config-panel-header">
                <div className="config-subpanel-header">
                    
                    <h3>Z-score threshold</h3>
                    <p>Flag records exceed this deviation</p>
                </div>
                <input type="number"></input>
            </div>
            <hr />
        </div>
                

        <div className="panel">
            <div className="config-panel-header">
                <h2>ML MODELS</h2>
                <div className="panel-header-buttons">
                   
                </div>
            </div>

        </div>

        </>
        )
}
