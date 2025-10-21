import React, { useState, useEffect } from 'react';
import { marketingAPI } from '../services/api';
import './Marketing.css';

const Marketing = ({ user }) => {
  const [activeTab, setActiveTab] = useState('campaigns');
  const [campaigns, setCampaigns] = useState([]);
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCampaignForm, setShowCampaignForm] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);

  const [campaignForm, setCampaignForm] = useState({
    name: '',
    type: 'email',
    budget: '',
    start_date: '',
    end_date: ''
  });

  const [leadForm, setLeadForm] = useState({
    name: '',
    email: '',
    phone: '',
    source: 'website',
    notes: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [campaignsRes, leadsRes] = await Promise.all([
        marketingAPI.getCampaigns(),
        marketingAPI.getLeads()
      ]);
      setCampaigns(campaignsRes.data);
      setLeads(leadsRes.data);
    } catch (error) {
      setError('Failed to load marketing data');
      console.error('Marketing error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCampaignSubmit = async (e) => {
    e.preventDefault();
    try {
      await marketingAPI.createCampaign({
        ...campaignForm,
        budget: parseFloat(campaignForm.budget)
      });
      setCampaignForm({
        name: '',
        type: 'email',
        budget: '',
        start_date: '',
        end_date: ''
      });
      setShowCampaignForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to create campaign');
    }
  };

  const handleLeadSubmit = async (e) => {
    e.preventDefault();
    try {
      await marketingAPI.addLead(leadForm);
      setLeadForm({
        name: '',
        email: '',
        phone: '',
        source: 'website',
        notes: ''
      });
      setShowLeadForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to add lead');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const tabs = [
    { id: 'campaigns', label: 'Campaigns', icon: 'fas fa-bullhorn' },
    { id: 'leads', label: 'Leads', icon: 'fas fa-user-plus' },
    { id: 'analytics', label: 'Analytics', icon: 'fas fa-chart-bar' }
  ];

  const campaignTypes = ['email', 'social', 'ads', 'content', 'event'];
  const leadSources = ['website', 'referral', 'campaign', 'social', 'cold_call', 'trade_show'];
  const leadStatuses = ['new', 'contacted', 'qualified', 'converted'];

  return (
    <div className="main-content">
      <div className="marketing-container">
        <div className="page-header">
          <h1>
            <i className="fas fa-bullhorn"></i>
            Marketing
          </h1>
          <p>Manage campaigns, leads, and marketing analytics</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <i className={tab.icon}></i>
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === 'analytics' && (
          <div className="tab-content">
            <div className="marketing-stats">
              <div className="stat-card">
                <div className="stat-icon campaigns">
                  <i className="fas fa-bullhorn"></i>
                </div>
                <div className="stat-content">
                  <h3>{campaigns.length}</h3>
                  <p>Total Campaigns</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon active-campaigns">
                  <i className="fas fa-play"></i>
                </div>
                <div className="stat-content">
                  <h3>{campaigns.filter(c => c.status === 'active').length}</h3>
                  <p>Active Campaigns</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon leads">
                  <i className="fas fa-user-plus"></i>
                </div>
                <div className="stat-content">
                  <h3>{leads.length}</h3>
                  <p>Total Leads</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon budget">
                  <i className="fas fa-dollar-sign"></i>
                </div>
                <div className="stat-content">
                  <h3>
                    {formatCurrency(campaigns.reduce((sum, c) => sum + (c.budget || 0), 0))}
                  </h3>
                  <p>Total Budget</p>
                </div>
              </div>
            </div>

            <div className="analytics-grid">
              <div className="card">
                <h3>Campaign Performance</h3>
                <div className="campaign-performance">
                  {campaigns.map(campaign => (
                    <div key={campaign.id} className="performance-item">
                      <div className="campaign-info">
                        <strong>{campaign.name}</strong>
                        <small>{campaign.type} • {campaign.status}</small>
                      </div>
                      <div className="campaign-budget">
                        {campaign.budget ? formatCurrency(campaign.budget) : 'No budget'}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <h3>Lead Sources</h3>
                <div className="lead-sources">
                  {leadSources.map(source => {
                    const count = leads.filter(lead => lead.source === source).length;
                    const percentage = leads.length > 0 ? (count / leads.length * 100).toFixed(1) : 0;
                    return (
                      <div key={source} className="source-item">
                        <div className="source-info">
                          <span>{source.replace('_', ' ')}</span>
                          <small>{count} leads ({percentage}%)</small>
                        </div>
                        <div className="source-bar">
                          <div 
                            className="source-fill" 
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="card">
                <h3>Lead Status Distribution</h3>
                <div className="status-distribution">
                  {leadStatuses.map(status => {
                    const count = leads.filter(lead => lead.status === status).length;
                    return (
                      <div key={status} className="status-item">
                        <span className={`status-badge status-${status}`}>
                          {status}
                        </span>
                        <strong>{count}</strong>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'campaigns' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Marketing Campaigns</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowCampaignForm(true)}
              >
                <i className="fas fa-plus"></i>
                Create Campaign
              </button>
            </div>

            {showCampaignForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Create Campaign</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowCampaignForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleCampaignSubmit}>
                    <div className="form-group">
                      <label>Campaign Name</label>
                      <input
                        type="text"
                        className="form-control"
                        value={campaignForm.name}
                        onChange={(e) => setCampaignForm({...campaignForm, name: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Type</label>
                        <select
                          className="form-control"
                          value={campaignForm.type}
                          onChange={(e) => setCampaignForm({...campaignForm, type: e.target.value})}
                        >
                          {campaignTypes.map(type => (
                            <option key={type} value={type}>
                              {type.charAt(0).toUpperCase() + type.slice(1)}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Budget</label>
                        <input
                          type="number"
                          step="0.01"
                          className="form-control"
                          value={campaignForm.budget}
                          onChange={(e) => setCampaignForm({...campaignForm, budget: e.target.value})}
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Start Date</label>
                        <input
                          type="date"
                          className="form-control"
                          value={campaignForm.start_date}
                          onChange={(e) => setCampaignForm({...campaignForm, start_date: e.target.value})}
                        />
                      </div>
                      <div className="form-group">
                        <label>End Date</label>
                        <input
                          type="date"
                          className="form-control"
                          value={campaignForm.end_date}
                          onChange={(e) => setCampaignForm({...campaignForm, end_date: e.target.value})}
                        />
                      </div>
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowCampaignForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Create Campaign
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Budget</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map(campaign => (
                    <tr key={campaign.id}>
                      <td><strong>{campaign.name}</strong></td>
                      <td>
                        <span className={`type-badge type-${campaign.type}`}>
                          {campaign.type}
                        </span>
                      </td>
                      <td>{campaign.budget ? formatCurrency(campaign.budget) : '-'}</td>
                      <td>{campaign.start_date ? formatDate(campaign.start_date) : '-'}</td>
                      <td>{campaign.end_date ? formatDate(campaign.end_date) : '-'}</td>
                      <td>
                        <span className={`status-badge status-${campaign.status}`}>
                          {campaign.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'leads' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Lead Management</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowLeadForm(true)}
              >
                <i className="fas fa-plus"></i>
                Add Lead
              </button>
            </div>

            {showLeadForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Add Lead</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowLeadForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleLeadSubmit}>
                    <div className="form-group">
                      <label>Name</label>
                      <input
                        type="text"
                        className="form-control"
                        value={leadForm.name}
                        onChange={(e) => setLeadForm({...leadForm, name: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Email</label>
                        <input
                          type="email"
                          className="form-control"
                          value={leadForm.email}
                          onChange={(e) => setLeadForm({...leadForm, email: e.target.value})}
                        />
                      </div>
                      <div className="form-group">
                        <label>Phone</label>
                        <input
                          type="tel"
                          className="form-control"
                          value={leadForm.phone}
                          onChange={(e) => setLeadForm({...leadForm, phone: e.target.value})}
                        />
                      </div>
                    </div>
                    <div className="form-group">
                      <label>Source</label>
                      <select
                        className="form-control"
                        value={leadForm.source}
                        onChange={(e) => setLeadForm({...leadForm, source: e.target.value})}
                      >
                        {leadSources.map(source => (
                          <option key={source} value={source}>
                            {source.replace('_', ' ').charAt(0).toUpperCase() + source.replace('_', ' ').slice(1)}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Notes</label>
                      <textarea
                        className="form-control"
                        rows="3"
                        value={leadForm.notes}
                        onChange={(e) => setLeadForm({...leadForm, notes: e.target.value})}
                      ></textarea>
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowLeadForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Add Lead
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Contact</th>
                    <th>Source</th>
                    <th>Status</th>
                    <th>Notes</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map(lead => (
                    <tr key={lead.id}>
                      <td><strong>{lead.name}</strong></td>
                      <td>
                        <div>
                          {lead.email && <div>{lead.email}</div>}
                          {lead.phone && <div>{lead.phone}</div>}
                        </div>
                      </td>
                      <td>
                        <span className={`source-badge source-${lead.source}`}>
                          {lead.source.replace('_', ' ')}
                        </span>
                      </td>
                      <td>
                        <span className={`status-badge status-${lead.status}`}>
                          {lead.status}
                        </span>
                      </td>
                      <td>
                        <div className="notes-cell">
                          {lead.notes || '-'}
                        </div>
                      </td>
                      <td>{formatDate(lead.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Marketing;