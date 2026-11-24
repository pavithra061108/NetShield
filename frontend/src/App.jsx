import { useEffect, useState } from "react";
import axios from "axios";

import {
  Shield,
  LayoutDashboard,
  Activity,
  Network,
  BrainCircuit,
  Bell,
  BarChart3,
  BadgeCheck,
  FileText,
  Settings,
  RefreshCw,
  Download,
  Search,
  Database,
  Server
} from "lucide-react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const navigation = [
  ["Overview", LayoutDashboard],
  ["Traffic Analysis", Activity],
  ["Network Flows", Network],
  ["ML Predictions", BrainCircuit],
  ["Security Alerts", Bell],
  ["Model Performance", BarChart3],
  ["Feature Validation", BadgeCheck],
  ["Reports", FileText],
  ["Settings", Settings]
];

function App() {
  const [page, setPage] = useState("Overview");
  const [stats, setStats] = useState({});
  const [flows, setFlows] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [model, setModel] = useState({});
  const [validation, setValidation] = useState({});
  const [online, setOnline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [health, s, f, a, m, v] = await Promise.all([
        axios.get(`${API}/health`),
        axios.get(`${API}/statistics`),
        axios.get(`${API}/flows`),
        axios.get(`${API}/alerts`),
        axios.get(`${API}/model`),
        axios.get(`${API}/validation`)
      ]);

      setOnline(health.data.status === "healthy");
      setStats(s.data);
      setFlows(f.data);
      setAlerts(a.data);
      setModel(m.data);
      setValidation(v.data);
    } catch {
      setOnline(false);
      setMessage("Unable to load dashboard data.");
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function runAnalysis() {
    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(`${API}/analyze`);

      setMessage(
        `Offline analysis completed. ${response.data.processed} records processed.`
      );

      await loadData();
    } catch {
      setMessage("Analysis failed. Check the backend terminal.");
    } finally {
      setLoading(false);
    }
  }

  function exportCSV() {
    const escape = value =>
      `"${String(value ?? "").replaceAll('"', '""')}"`;

    const rows = [
      ["ID", "Timestamp", "Source", "Label", "Model Score"],
      ...flows.map(f => [
        f.id,
        f.timestamp,
        f.source_file,
        f.label,
        f.probability
      ])
    ];

    const csv = rows
      .map(row => row.map(escape).join(","))
      .join("\n");

    const url = URL.createObjectURL(
      new Blob([csv], { type: "text/csv" })
    );

    const link = document.createElement("a");
    link.href = url;
    link.download = "netshield_report.csv";
    link.click();

    URL.revokeObjectURL(url);
  }

  const distribution = [
    { name: "Benign", value: stats.benign_flows || 0 },
    { name: "Flagged", value: stats.flagged_flows || 0 }
  ];

  const modelMetrics = [
    { name: "Accuracy", value: model.accuracy || 0 },
    { name: "Precision", value: model.precision || 0 },
    { name: "Recall", value: model.recall || 0 },
    { name: "F1 Score", value: model.f1_score || 0 }
  ];

  const trafficData = flows.slice(0, 15).reverse().map(f => ({
    name: `#${f.id}`,
    packets:
      Number(f.features?.["Total Fwd Packets"] || 0) +
      Number(f.features?.["Total Backward Packets"] || 0)
  }));

  function Card({ title, value, icon: Icon, color }) {
    return (
      <div className="stat-card">
        <div className="card-icon" style={{ color }}>
          <Icon size={25} />
        </div>
        <p>{title}</p>
        <h2>{value}</h2>
      </div>
    );
  }

  function FlowTable({ records }) {
    const filtered = records.filter(f =>
      JSON.stringify(f).toLowerCase().includes(search.toLowerCase())
    );

    return (
      <div className="panel">
        <div className="table-header">
          <h3>Analysis Records</h3>

          <div className="search-box">
            <Search size={17} />
            <input
              placeholder="Search records..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
        </div>

        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Source</th>
                <th>Timestamp</th>
                <th>Classification</th>
                <th>Model Score</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map(f => (
                <tr key={f.id}>
                  <td>#{f.id}</td>
                  <td>{f.source_file}</td>
                  <td>{new Date(f.timestamp).toLocaleString()}</td>
                  <td>
                    <span className={
                      f.label === "ATTACK" ? "badge danger" : "badge success"
                    }>
                      {f.label === "ATTACK" ? "FLAGGED" : f.label}
                    </span>
                  </td>
                  <td>
                    {(Number(f.probability) * 100).toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {!filtered.length && (
            <p className="empty">No matching records available.</p>
          )}
        </div>
      </div>
    );
  }

  function TrafficChart() {
    return (
      <div className="panel">
        <h3>Packet Counts by Offline Record</h3>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={trafficData}>
            <CartesianGrid stroke="#233249" strokeDasharray="3 3" />
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Bar dataKey="packets" fill="#22d3ee" radius={[5, 5, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="app">

      <aside className="sidebar">
        <div className="brand">
          <Shield size={34} />
          <div>
            <h2>NetShield</h2>
            <small>SECURITY ANALYTICS</small>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>

        {navigation.map(([name, Icon]) => (
          <button
            key={name}
            className={`nav-item ${page === name ? "active" : ""}`}
            onClick={() => {
              setPage(name);
              setSearch("");
            }}
          >
            <Icon size={19} />
            {name}
          </button>
        ))}

        <div className="sidebar-footer">
          <span className={`dot ${online ? "green" : "red"}`} />
          {online ? "Backend Connected" : "Backend Unavailable"}
        </div>
      </aside>

      <main className="main-content">

        <header className="topbar">
          <div>
            <h1>{page}</h1>
            <p>NetShield Offline Security Analytics</p>
          </div>

          <div className="actions">
            <button className="secondary" onClick={loadData}>
              <RefreshCw size={17} /> Refresh
            </button>

            <button
              className="primary"
              onClick={runAnalysis}
              disabled={loading}
            >
              <Activity size={18} />
              {loading ? "Processing..." : "Run Analysis"}
            </button>
          </div>
        </header>

        <div className="notice">
          Offline demonstration using saved synthetic test data.
          Model flags are not confirmed security incidents.
        </div>

        {message && <div className="notice">{message}</div>}

        {page === "Overview" && (
          <>
            <div className="cards">
              <Card title="Total Records" value={stats.total_flows || 0}
                icon={Network} color="#22d3ee" />

              <Card title="Benign Records" value={stats.benign_flows || 0}
                icon={Shield} color="#34d399" />

              <Card title="Flagged Records" value={stats.flagged_flows || 0}
                icon={Bell} color="#f87171" />

              <Card title="Feature Agreement"
                value={`${validation.agreement_percentage ?? 0}%`}
                icon={BadgeCheck} color="#a78bfa" />
            </div>

            <div className="chart-grid">
              <div className="panel">
                <h3>Classification Distribution</h3>

                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={distribution}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={65}
                      outerRadius={100}
                      label
                    >
                      <Cell fill="#34d399" />
                      <Cell fill="#f87171" />
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <TrafficChart />
            </div>

            <FlowTable records={flows.slice(0, 10)} />
          </>
        )}

        {page === "Traffic Analysis" && <TrafficChart />}

        {page === "Network Flows" && <FlowTable records={flows} />}

        {page === "ML Predictions" && (
          <FlowTable records={flows} />
        )}

        {page === "Security Alerts" && (
          <FlowTable records={alerts} />
        )}

        {page === "Model Performance" && (
          <>
            <div className="cards">
              {modelMetrics.map(m => (
                <Card
                  key={m.name}
                  title={m.name}
                  value={`${m.value}%`}
                  icon={BrainCircuit}
                  color="#22d3ee"
                />
              ))}
            </div>

            <div className="panel">
              <h3>Random Forest Evaluation</h3>

              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={modelMetrics}>
                  <CartesianGrid stroke="#233249" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis domain={[0, 100]} stroke="#94a3b8" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#22d3ee" />
                </BarChart>
              </ResponsiveContainer>

              <p className="muted">
                Results from a random held-out dataset split.
                Independent real-world performance is not established.
              </p>
            </div>
          </>
        )}

        {page === "Feature Validation" && (
          <>
            <div className="cards">
              <Card title="Passed" value={validation.passed ?? "—"}
                icon={BadgeCheck} color="#34d399" />

              <Card title="Failed" value={validation.failed ?? "—"}
                icon={Activity} color="#f87171" />

              <Card title="Undefined" value={validation.undefined ?? "—"}
                icon={Database} color="#fbbf24" />

              <Card title="Status"
                value={validation.validation_status || "Unknown"}
                icon={Shield} color="#22d3ee" />
            </div>

            <div className="panel">
              <h3>CICFlowMeter Compatibility Report</h3>
              <pre>{JSON.stringify(validation, null, 2)}</pre>
            </div>
          </>
        )}

        {page === "Reports" && (
          <div className="panel">
            <h3>Export Analysis Report</h3>
            <p className="muted">
              Download stored offline analysis records in CSV format.
            </p>

            <button className="primary" onClick={exportCSV}>
              <Download size={18} /> Download CSV
            </button>
          </div>
        )}

        {page === "Settings" && (
          <div className="panel">
            <h3>System Configuration</h3>

            <div className="setting-row">
              <Server size={20} />
              Backend: {online ? "Connected" : "Unavailable"}
            </div>

            <div className="setting-row">
              <Database size={20} />
              Database: SQLite
            </div>

            <div className="setting-row">
              <BrainCircuit size={20} />
              Model: Random Forest
            </div>

            <div className="setting-row">
              <Shield size={20} />
              Mode: Offline Demonstration
            </div>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;