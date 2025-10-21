import React, { useState, useEffect } from 'react';
import { financeAPI } from '../services/api';
import './Finance.css';

const Finance = ({ user }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [records, setRecords] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showRecordForm, setShowRecordForm] = useState(false);
  const [showInvoiceForm, setShowInvoiceForm] = useState(false);

  const [recordForm, setRecordForm] = useState({
    type: 'income',
    amount: '',
    description: '',
    category: ''
  });

  const [invoiceForm, setInvoiceForm] = useState({
    client_name: '',
    client_email: '',
    amount: '',
    due_date: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [recordsRes, invoicesRes] = await Promise.all([
        financeAPI.getRecords(),
        financeAPI.getInvoices()
      ]);
      setRecords(recordsRes.data);
      setInvoices(invoicesRes.data);
    } catch (error) {
      setError('Failed to load finance data');
      console.error('Finance error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRecordSubmit = async (e) => {
    e.preventDefault();
    try {
      await financeAPI.addRecord({
        ...recordForm,
        amount: parseFloat(recordForm.amount)
      });
      setRecordForm({ type: 'income', amount: '', description: '', category: '' });
      setShowRecordForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to add record');
    }
  };

  const handleInvoiceSubmit = async (e) => {
    e.preventDefault();
    try {
      await financeAPI.createInvoice({
        ...invoiceForm,
        amount: parseFloat(invoiceForm.amount)
      });
      setInvoiceForm({ client_name: '', client_email: '', amount: '', due_date: '' });
      setShowInvoiceForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to create invoice');
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

  const calculateTotals = () => {
    const totalIncome = records
      .filter(r => r.type === 'income')
      .reduce((sum, r) => sum + r.amount, 0);
    
    const totalExpenses = records
      .filter(r => r.type === 'expense')
      .reduce((sum, r) => sum + r.amount, 0);
    
    return { totalIncome, totalExpenses, netProfit: totalIncome - totalExpenses };
  };

  const { totalIncome, totalExpenses, netProfit } = calculateTotals();

  const tabs = [
    { id: 'overview', label: 'Overview', icon: 'fas fa-chart-pie' },
    { id: 'records', label: 'Records', icon: 'fas fa-list' },
    { id: 'invoices', label: 'Invoices', icon: 'fas fa-file-invoice' }
  ];

  return (
    <div className="main-content">
      <div className="finance-container">
        <div className="page-header">
          <h1>
            <i className="fas fa-chart-line"></i>
            Finance Management
          </h1>
          <p>Track your income, expenses, and invoices</p>
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

        {activeTab === 'overview' && (
          <div className="tab-content">
            <div className="finance-stats">
              <div className="stat-card income">
                <div className="stat-icon">
                  <i className="fas fa-arrow-up"></i>
                </div>
                <div className="stat-content">
                  <h3>{formatCurrency(totalIncome)}</h3>
                  <p>Total Income</p>
                </div>
              </div>

              <div className="stat-card expense">
                <div className="stat-icon">
                  <i className="fas fa-arrow-down"></i>
                </div>
                <div className="stat-content">
                  <h3>{formatCurrency(totalExpenses)}</h3>
                  <p>Total Expenses</p>
                </div>
              </div>

              <div className="stat-card profit">
                <div className="stat-icon">
                  <i className="fas fa-chart-line"></i>
                </div>
                <div className="stat-content">
                  <h3 className={netProfit >= 0 ? 'positive' : 'negative'}>
                    {formatCurrency(netProfit)}
                  </h3>
                  <p>Net Profit</p>
                </div>
              </div>
            </div>

            <div className="overview-grid">
              <div className="card">
                <h3>Recent Transactions</h3>
                <div className="recent-transactions">
                  {records.slice(0, 5).map(record => (
                    <div key={record.id} className="transaction-item">
                      <div className="transaction-info">
                        <strong>{record.description}</strong>
                        <small>{record.category}</small>
                      </div>
                      <div className={`transaction-amount ${record.type}`}>
                        {record.type === 'income' ? '+' : '-'}{formatCurrency(record.amount)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <h3>Invoice Status</h3>
                <div className="invoice-summary">
                  <div className="summary-item">
                    <span>Pending Invoices</span>
                    <strong>{invoices.filter(i => i.status === 'pending').length}</strong>
                  </div>
                  <div className="summary-item">
                    <span>Paid Invoices</span>
                    <strong>{invoices.filter(i => i.status === 'paid').length}</strong>
                  </div>
                  <div className="summary-item">
                    <span>Total Invoice Value</span>
                    <strong>
                      {formatCurrency(invoices.reduce((sum, i) => sum + i.amount, 0))}
                    </strong>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'records' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Financial Records</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowRecordForm(true)}
              >
                <i className="fas fa-plus"></i>
                Add Record
              </button>
            </div>

            {showRecordForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Add Financial Record</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowRecordForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleRecordSubmit}>
                    <div className="form-group">
                      <label>Type</label>
                      <select
                        className="form-control"
                        value={recordForm.type}
                        onChange={(e) => setRecordForm({...recordForm, type: e.target.value})}
                      >
                        <option value="income">Income</option>
                        <option value="expense">Expense</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Amount</label>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control"
                        value={recordForm.amount}
                        onChange={(e) => setRecordForm({...recordForm, amount: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Description</label>
                      <input
                        type="text"
                        className="form-control"
                        value={recordForm.description}
                        onChange={(e) => setRecordForm({...recordForm, description: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Category</label>
                      <input
                        type="text"
                        className="form-control"
                        value={recordForm.category}
                        onChange={(e) => setRecordForm({...recordForm, category: e.target.value})}
                      />
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowRecordForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Add Record
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
                    <th>Date</th>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map(record => (
                    <tr key={record.id}>
                      <td>{formatDate(record.date)}</td>
                      <td>
                        <span className={`status-badge status-${record.type}`}>
                          {record.type}
                        </span>
                      </td>
                      <td>{record.description}</td>
                      <td>{record.category}</td>
                      <td className={`amount ${record.type}`}>
                        {record.type === 'income' ? '+' : '-'}{formatCurrency(record.amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'invoices' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Invoices</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowInvoiceForm(true)}
              >
                <i className="fas fa-plus"></i>
                Create Invoice
              </button>
            </div>

            {showInvoiceForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Create Invoice</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowInvoiceForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleInvoiceSubmit}>
                    <div className="form-group">
                      <label>Client Name</label>
                      <input
                        type="text"
                        className="form-control"
                        value={invoiceForm.client_name}
                        onChange={(e) => setInvoiceForm({...invoiceForm, client_name: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Client Email</label>
                      <input
                        type="email"
                        className="form-control"
                        value={invoiceForm.client_email}
                        onChange={(e) => setInvoiceForm({...invoiceForm, client_email: e.target.value})}
                      />
                    </div>
                    <div className="form-group">
                      <label>Amount</label>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control"
                        value={invoiceForm.amount}
                        onChange={(e) => setInvoiceForm({...invoiceForm, amount: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Due Date</label>
                      <input
                        type="date"
                        className="form-control"
                        value={invoiceForm.due_date}
                        onChange={(e) => setInvoiceForm({...invoiceForm, due_date: e.target.value})}
                      />
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowInvoiceForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Create Invoice
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
                    <th>Invoice #</th>
                    <th>Client</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Due Date</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map(invoice => (
                    <tr key={invoice.id}>
                      <td>{invoice.invoice_number}</td>
                      <td>
                        <div>
                          <strong>{invoice.client_name}</strong>
                          {invoice.client_email && <br />}
                          <small>{invoice.client_email}</small>
                        </div>
                      </td>
                      <td>{formatCurrency(invoice.amount)}</td>
                      <td>
                        <span className={`status-badge status-${invoice.status}`}>
                          {invoice.status}
                        </span>
                      </td>
                      <td>{invoice.due_date ? formatDate(invoice.due_date) : '-'}</td>
                      <td>{formatDate(invoice.created_at)}</td>
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

export default Finance;