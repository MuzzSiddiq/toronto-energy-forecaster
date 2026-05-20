import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, Thermometer, Zap, Settings2 } from 'lucide-react';

function App() {

  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  const [history, setHistory] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);

  // --- Simulator State ---
  const [simParams, setSimParams] = useState({
    temp: 20,
    humidity: 50,
    wind_speed: 15,
    hour: 12,
    day_of_week: 1,
    is_weekend: 0
  });
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const fetchHistory = axios.get(`${API_URL}/history?limit=72`);
    const fetchForecast = axios.get(`${API_URL}/forecast`);

    Promise.all([fetchHistory, fetchForecast])
      .then(([historyRes, forecastRes]) => {
        setHistory(historyRes.data.reverse());
        setForecast(forecastRes.data);
        setLoading(false);
      })
      .catch(err => console.error("API Error:", err));
  }, [API_URL]);

  const runSimulation = () => {
    axios.post(`${API_URL}/predict`, simParams)
      .then(res => setPrediction(res.data.predicted_demand_mw))
      .catch(err => console.error("Simulation Error:", err));
  };

  if (loading) return <div className="p-10 text-center">Synchronizing with Toronto Grid...</div>;

  return (
      <div style={{padding: '40px', backgroundColor: '#f3f4f6', minHeight: '100vh', fontFamily: 'Inter, sans-serif'}}>

        {/* Header Block with Role Toggle */}
        <header style={{marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div>
            <h1 style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontSize: '2.2rem',
              color: '#111827',
              margin: 0
            }}>
              <Zap color="#eab308" fill="#eab308"/> Toronto Pulse
            </h1>
            <p style={{color: '#4b5563', marginTop: '5px'}}>
              {userRole === 'public'
                  ? 'Public Energy Transparency Portal'
                  : 'IESO Control Room & Predictive Simulation Engine'}
            </p>
          </div>

          {/* Role Toggle Switch */}
          <div style={{display: 'flex', gap: '10px', backgroundColor: '#e5e7eb', padding: '5px', borderRadius: '8px'}}>
            <button onClick={() => setUserRole('public')}
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      fontWeight: 'bold',
                      backgroundColor: userRole === 'public' ? '#3b82f6' : 'transparent',
                      color: userRole === 'public' ? 'white' : '#4b5563',
                      transition: 'all 0.2s'
                    }}>
              Public View
            </button>
            <button onClick={() => setUserRole('operator')}
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      fontWeight: 'bold',
                      backgroundColor: userRole === 'operator' ? '#1f2937' : 'transparent',
                      color: userRole === 'operator' ? 'white' : '#4b5563',
                      transition: 'all 0.2s'
                    }}>
              Grid Operator View
            </button>
          </div>
        </header>

        {/* DYNAMIC TWO-WAY VIEW LAYOUT */}
        <div style={{display: 'grid', gridTemplateColumns: userRole === 'operator' ? '3fr 1fr' : '1fr', gap: '25px'}}>

          {/* Left Column: Charts (Visible to BOTH, but styled slightly differently) */}
          <div style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
            <div style={containerStyle}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '20px'
              }}>
                <h3 style={{margin: 0}}>Grid Load: Actual vs. AI Forecast</h3>

                {/* Public-only Quick Status Badge */}
                {userRole === 'public' && (
                    <span style={{
                      backgroundColor: '#d1fae5',
                      color: '#065f46',
                      padding: '6px 12px',
                      borderRadius: '20px',
                      fontSize: '0.85rem',
                      fontWeight: 'bold',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px'
                    }}>
                  ● System Status: Stable
                </span>
                )}
              </div>

              <div style={{width: '100%', height: 400}}>
                <ResponsiveContainer>
                  <LineChart data={[...history, ...forecast]}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb"/>
                    <XAxis dataKey="timestamp" tickFormatter={(str) => new Date(str).toLocaleDateString([], {
                      month: 'short',
                      day: 'numeric'
                    })}/>
                    <YAxis domain={['auto', 'auto']} label={{value: 'MW', angle: -90, position: 'insideLeft'}}/>
                    <Tooltip contentStyle={{
                      borderRadius: '12px',
                      border: 'none',
                      boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'
                    }}/>
                    <Legend verticalAlign="top" height={36}/>
                    <Line name="Actual History" type="monotone" dataKey="demand" stroke="#3b82f6" strokeWidth={3}
                          dot={false}/>
                    <Line name="7-Day Forecast" type="monotone" dataKey="predicted_demand" stroke="#10b981"
                          strokeWidth={3} strokeDasharray="8 5" dot={false}/>
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Right Column: Simulator (CONDITIONAL: ONLY visible to Grid Operators) */}
          {userRole === 'operator' && (
              <div style={containerStyle}>
                <h3 style={{marginTop: 0, display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px'}}>
                  <Settings2 size={20}/> Grid Stress-Test
                </h3>
                <p style={{fontSize: '0.8rem', color: '#6b7280', marginBottom: '15px'}}>
                  Authorized Personnel Only. Simulate extreme weather vectors to test grid capacity thresholds.
                </p>

                <div style={inputGroupStyle}>
                  <label>Temp: {simParams.temp}°C</label>
                  <input type="range" min="-30" max="40" value={simParams.temp}
                         onChange={(e) => setSimParams({...simParams, temp: parseFloat(e.target.value)})}/>
                </div>

                <div style={inputGroupStyle}>
                  <label>Humidity: {simParams.humidity}%</label>
                  <input type="range" min="0" max="100" value={simParams.humidity}
                         onChange={(e) => setSimParams({...simParams, humidity: parseFloat(e.target.value)})}/>
                </div>

                <button onClick={runSimulation} style={{...buttonStyle, backgroundColor: '#1f2937'}}>Run AI Inference
                </button>

                {prediction && (
                    <div style={resultStyle}>
                      <span style={{fontSize: '0.8rem', color: '#6b7280'}}>Predicted Peak Load:</span>
                      <div style={{fontSize: '1.8rem', fontWeight: 'bold', color: '#10b981'}}>{prediction} MW</div>

                      {/* Dynamic Danger Alert for the Operator */}
                      {prediction > 6000 && (
                          <div style={{
                            marginTop: '10px',
                            backgroundColor: '#fee2e2',
                            color: '#991b1b',
                            padding: '8px',
                            borderRadius: '6px',
                            fontSize: '0.75rem',
                            fontWeight: 'bold'
                          }}>
                            ⚠️ CRITICAL DEMAND THRESHOLD EXCEEDED
                          </div>
                      )}
                    </div>
                )}
              </div>
          )}

        </div>
      </div>
  );
}

// --- Styles ---
const containerStyle = {
  backgroundColor: 'white',
  padding: '25px',
  borderRadius: '16px',
  boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'
};
const inputGroupStyle = {marginBottom: '20px', display: 'flex', flexDirection: 'column', gap: '8px'};
const buttonStyle = {
  width: '100%',
  padding: '12px',
  backgroundColor: '#3b82f6',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  fontWeight: '600',
  cursor: 'pointer',
  marginTop: '10px'
};
const resultStyle = {
  marginTop: '25px',
  padding: '15px',
  backgroundColor: '#f0fdf4',
  borderRadius: '8px',
  border: '1px solid #bbf7d0',
  textAlign: 'center'
};

export default App;