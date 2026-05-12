import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, Thermometer, Zap } from 'lucide-react';

function App() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch last 48 hours of data from your FastAPI backend
    axios.get('http://127.0.0.1:8000/history?limit=48')
      .then(res => {
        const sortedData = res.data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        setHistory(sortedData);
        setLoading(false);
      })
      .catch(err => console.error("API Error:", err));
  }, []);

  if (loading) return <div className="p-10 text-center">Powering up the grid...</div>;

  return (
    <div style={{ padding: '40px', backgroundColor: '#f9fafb', minHeight: '100vh', fontFamily: 'Inter, sans-serif' }}>
      <header style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '2rem', color: '#111827' }}>
          <Zap color="#eab308" fill="#eab308" /> Toronto Pulse
        </h1>
        <p style={{ color: '#6b7280' }}>Real-time Grid Demand Monitoring & Forecasting</p>
      </header>

      {/* Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '40px' }}>
        <div style={cardStyle}>
          <Activity size={20} color="#3b82f6" />
          <span style={labelStyle}>Current Demand</span>
          <h2 style={valueStyle}>{history[history.length - 1]?.demand} MW</h2>
        </div>
        <div style={cardStyle}>
          <Thermometer size={20} color="#ef4444" />
          <span style={labelStyle}>System Status</span>
          <h2 style={valueStyle}>Stable</h2>
        </div>
      </div>

      {/* The Chart */}
      <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <h3 style={{ marginBottom: '20px' }}>Historical Demand (Last 48 Hours)</h3>
        <div style={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
              <XAxis
                dataKey="timestamp"
                tick={{fontSize: 12}}
                tickFormatter={(str) => new Date(str).getHours() + ":00"}
              />
              <YAxis domain={['auto', 'auto']} tick={{fontSize: 12}} />
              <Tooltip
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
              />
              <Legend />
              <Line
                name="Demand (MW)"
                type="monotone"
                dataKey="demand"
                stroke="#3b82f6"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

const cardStyle = { backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', display: 'flex', flexDirection: 'column', gap: '8px' };
const labelStyle = { fontSize: '0.875rem', color: '#6b7280', fontWeight: '500' };
const valueStyle = { margin: 0, fontSize: '1.5rem', fontWeight: 'bold', color: '#111827' };

export default App;