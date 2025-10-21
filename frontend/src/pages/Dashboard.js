import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dashboardAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats(response.data.stats);
    } catch (error) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const moduleCards = [
    {
      title: 'Finance',
      icon: 'fas fa-chart-line',
      description: 'Manage income, expenses, and invoices',
      link: '/finance',
      color: '#28a745'
    },
    {
      title: 'Human Resources',
      icon: 'fas fa-users',
      description: 'Employee management and tasks',
      link: '/hr',
      color: '#007bff'
    },
    {
      title: 'Marketing',
      icon: 'fas fa-bullhorn',
      description: 'Campaigns and lead management',
      link: '/marketing',
      color: '#fd7e14'
    },
    {
      title: 'Inventory',
      icon: 'fas fa-boxes',
      description: 'Product and stock management',
      link: '/inventory',
      color: '#6f42c1'
    }
  ];

  if (loading) {
    return (
      <div className="main-content">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Welcome back, {user.full_name}!</h1>
          <p>Here's what's happening with your business today.</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        {stats && (
          <div className="stats-grid">
            <div className="stat-card income">
              <div className="stat-icon">
                <i className="fas fa-arrow-up"></i>
              </div>
              <div className="stat-content">
                <h3>{formatCurrency(stats.total_income)}</h3>
                <p>Total Income</p>
              </div>
            </div>

            <div className="stat-card expense">
              <div className="stat-icon">
                <i className="fas fa-arrow-down"></i>
              </div>
              <div className="stat-content">
                <h3>{formatCurrency(stats.total_expenses)}</h3>
                <p>Total Expenses</p>
              </div>
            </div>

            <div className="stat-card profit">
              <div className="stat-icon">
                <i className="fas fa-chart-line"></i>
              </div>
              <div className="stat-content">
                <h3>{formatCurrency(stats.net_profit)}</h3>
                <p>Net Profit</p>
              </div>
            </div>

            <div className="stat-card employees">
              <div className="stat-icon">
                <i className="fas fa-users"></i>
              </div>
              <div className="stat-content">
                <h3>{stats.employee_count}</h3>
                <p>Active Employees</p>
              </div>
            </div>

            <div className="stat-card invoices">
              <div className="stat-icon">
                <i className="fas fa-file-invoice"></i>
              </div>
              <div className="stat-content">
                <h3>{stats.pending_invoices}</h3>
                <p>Pending Invoices</p>
              </div>
            </div>

            <div className="stat-card campaigns">
              <div className="stat-icon">
                <i className="fas fa-bullhorn"></i>
              </div>
              <div className="stat-content">
                <h3>{stats.active_campaigns}</h3>
                <p>Active Campaigns</p>
              </div>
            </div>

            <div className="stat-card products">
              <div className="stat-icon">
                <i className="fas fa-boxes"></i>
              </div>
              <div className="stat-content">
                <h3>{stats.total_products}</h3>
                <p>Total Products</p>
              </div>
            </div>
          </div>
        )}

        <div className="modules-section">
          <h2>ERP Modules</h2>
          <div className="modules-grid">
            {moduleCards.map((module) => (
              <Link 
                key={module.title}
                to={module.link} 
                className="module-card"
                style={{ '--module-color': module.color }}
              >
                <div className="module-icon">
                  <i className={module.icon}></i>
                </div>
                <div className="module-content">
                  <h3>{module.title}</h3>
                  <p>{module.description}</p>
                </div>
                <div className="module-arrow">
                  <i className="fas fa-arrow-right"></i>
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div className="company-info">
          <div className="card">
            <h3>Company Information</h3>
            <div className="company-details">
              <div className="detail-item">
                <strong>Company:</strong> {user.company?.name}
              </div>
              <div className="detail-item">
                <strong>Subscription:</strong> 
                <span className={`subscription-badge ${user.company?.subscription}`}>
                  {user.company?.subscription?.toUpperCase()}
                </span>
              </div>
              <div className="detail-item">
                <strong>Role:</strong> {user.role?.toUpperCase()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;