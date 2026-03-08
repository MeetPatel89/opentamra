import React from 'react';
import { NavLink } from 'react-router-dom';

function Sidebar() {
  return (
    <nav className="sidebar">
      <div className="sidebar-brand">OpenTAMRA</div>
      <ul className="sidebar-nav">
        <li><NavLink to="/">Dashboard</NavLink></li>
        <li><NavLink to="/jobs">Jobs</NavLink></li>
        <li><NavLink to="/jobs/new">New Job</NavLink></li>
      </ul>
    </nav>
  );
}

export default Sidebar;
