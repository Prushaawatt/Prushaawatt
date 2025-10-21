import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { authAPI } from '../services/api';
import './Navbar.css';

const Navbar = ({ user, onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      onLogout();
    } catch (error) {
      console.error('Logout error:', error);
      onLogout(); // Logout anyway
    }
  };

  const menuItems = [
    { path: '/dashboard', icon: 'fas fa-tachometer-alt', label: 'Dashboard' },
    { path: '/finance', icon: 'fas fa-chart-line', label: 'Finance' },
    { path: '/hr', icon: 'fas fa-users', label: 'HR' },
    { path: '/marketing', icon: 'fas fa-bullhorn', label: 'Marketing' },
    { path: '/inventory', icon: 'fas fa-boxes', label: 'Inventory' },
  ];

  return (
    <>
      <nav className="navbar">
        <div className="navbar-brand">
          <i className="fas fa-building"></i>
          <span>ERP System</span>
        </div>
        
        <div className="navbar-user">
          <span className="user-name">{user.full_name}</span>
          <div className="user-dropdown">
            <button className="user-menu-btn">
              <i className="fas fa-user-circle"></i>
            </button>
            <div className="dropdown-content">
              <div className="user-info">
                <strong>{user.full_name}</strong>
                <small>{user.email}</small>
                <small>{user.company?.name}</small>
              </div>
              <button onClick={handleLogout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i>
                Logout
              </button>
            </div>
          </div>
        </div>

        <button 
          className="mobile-menu-btn"
          onClick={() => setIsOpen(!isOpen)}
        >
          <i className="fas fa-bars"></i>
        </button>
      </nav>

      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-menu">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`menu-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              <i className={item.icon}></i>
              <span>{item.label}</span>
            </Link>
          ))}
        </div>
      </aside>

      {isOpen && <div className="sidebar-overlay" onClick={() => setIsOpen(false)}></div>}
    </>
  );
};

export default Navbar;