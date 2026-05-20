import '../styles/dashboard.css'

export function NavBar({ setActivePage, configOption = "file" }) {
    return (
        <>
            <div className="dash-header">
                <h2>Machine Learning Payroll Anomaly Detection System</h2>
                <div className="options">
                    <button onClick={() => setActivePage("dashboard")}>Analysis</button>
                    <button onClick={() => setActivePage("analytics")}>Analytics</button>
                    <button onClick={() => setActivePage("config")} disabled={configOption === "file"}>Config</button>
                </div>
            </div>
            <hr />
        </>
    )
}