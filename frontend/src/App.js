import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import DashboardPage from './pages/DashboardPage';
import NewJobPage from './pages/NewJobPage';
import JobsPage from './pages/JobsPage';
import ReportsPage from './pages/ReportsPage';
import './App.css';

function App() {
  return (
    <div className="app">
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/jobs/new" element={<NewJobPage />} />
          <Route path="/reports/:jobId" element={<ReportsPage />} />
        </Routes>
      </Layout>
    </div>
  );
}

export default App;
