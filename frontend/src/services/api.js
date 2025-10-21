import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/api/register', userData),
  login: (credentials) => api.post('/api/login', credentials),
  logout: () => api.post('/api/logout'),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard'),
};

// Finance API
export const financeAPI = {
  getRecords: () => api.get('/api/finance/records'),
  addRecord: (record) => api.post('/api/finance/records', record),
  getInvoices: () => api.get('/api/finance/invoices'),
  createInvoice: (invoice) => api.post('/api/finance/invoices', invoice),
};

// HR API
export const hrAPI = {
  getEmployees: () => api.get('/api/hr/employees'),
  addEmployee: (employee) => api.post('/api/hr/employees', employee),
  getTasks: () => api.get('/api/hr/tasks'),
  createTask: (task) => api.post('/api/hr/tasks', task),
};

// Marketing API
export const marketingAPI = {
  getCampaigns: () => api.get('/api/marketing/campaigns'),
  createCampaign: (campaign) => api.post('/api/marketing/campaigns', campaign),
  getLeads: () => api.get('/api/marketing/leads'),
  addLead: (lead) => api.post('/api/marketing/leads', lead),
};

// Inventory API
export const inventoryAPI = {
  getProducts: () => api.get('/api/inventory/products'),
  addProduct: (product) => api.post('/api/inventory/products', product),
  recordStockMovement: (movement) => api.post('/api/inventory/stock-movement', movement),
};

export default api;