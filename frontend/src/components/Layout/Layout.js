import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import './Layout.css';

function Layout({ children }) {
  return (
    <>
      <Sidebar />
      <div className="main-content">
        <Header />
        {children}
      </div>
    </>
  );
}

export default Layout;
