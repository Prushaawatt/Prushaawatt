import React, { useState, useEffect } from 'react';
import { inventoryAPI } from '../services/api';
import './Inventory.css';

const Inventory = ({ user }) => {
  const [activeTab, setActiveTab] = useState('products');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showProductForm, setShowProductForm] = useState(false);
  const [showStockForm, setShowStockForm] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  const [productForm, setProductForm] = useState({
    name: '',
    sku: '',
    category: '',
    price: '',
    quantity: '',
    min_stock: '',
    description: ''
  });

  const [stockForm, setStockForm] = useState({
    product_id: '',
    type: 'in',
    quantity: '',
    reason: ''
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await inventoryAPI.getProducts();
      setProducts(response.data);
    } catch (error) {
      setError('Failed to load inventory data');
      console.error('Inventory error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    try {
      await inventoryAPI.addProduct({
        ...productForm,
        price: parseFloat(productForm.price),
        quantity: parseInt(productForm.quantity),
        min_stock: parseInt(productForm.min_stock)
      });
      setProductForm({
        name: '',
        sku: '',
        category: '',
        price: '',
        quantity: '',
        min_stock: '',
        description: ''
      });
      setShowProductForm(false);
      fetchProducts();
    } catch (error) {
      setError('Failed to add product');
    }
  };

  const handleStockSubmit = async (e) => {
    e.preventDefault();
    try {
      await inventoryAPI.recordStockMovement({
        ...stockForm,
        product_id: parseInt(stockForm.product_id),
        quantity: parseInt(stockForm.quantity)
      });
      setStockForm({
        product_id: '',
        type: 'in',
        quantity: '',
        reason: ''
      });
      setShowStockForm(false);
      fetchProducts();
    } catch (error) {
      setError('Failed to record stock movement');
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

  const getStockStatus = (product) => {
    if (product.quantity <= 0) return 'out-of-stock';
    if (product.quantity <= product.min_stock) return 'low-stock';
    return 'in-stock';
  };

  const getStockStatusLabel = (status) => {
    switch (status) {
      case 'out-of-stock': return 'Out of Stock';
      case 'low-stock': return 'Low Stock';
      case 'in-stock': return 'In Stock';
      default: return 'Unknown';
    }
  };

  const tabs = [
    { id: 'products', label: 'Products', icon: 'fas fa-boxes' },
    { id: 'overview', label: 'Overview', icon: 'fas fa-chart-pie' }
  ];

  const categories = [...new Set(products.map(p => p.category).filter(Boolean))];
  const lowStockProducts = products.filter(p => p.quantity <= p.min_stock);
  const outOfStockProducts = products.filter(p => p.quantity <= 0);

  return (
    <div className="main-content">
      <div className="inventory-container">
        <div className="page-header">
          <h1>
            <i className="fas fa-boxes"></i>
            Inventory Management
          </h1>
          <p>Track products, stock levels, and inventory movements</p>
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
            <div className="inventory-stats">
              <div className="stat-card">
                <div className="stat-icon products">
                  <i className="fas fa-boxes"></i>
                </div>
                <div className="stat-content">
                  <h3>{products.length}</h3>
                  <p>Total Products</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon categories">
                  <i className="fas fa-tags"></i>
                </div>
                <div className="stat-content">
                  <h3>{categories.length}</h3>
                  <p>Categories</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon low-stock">
                  <i className="fas fa-exclamation-triangle"></i>
                </div>
                <div className="stat-content">
                  <h3>{lowStockProducts.length}</h3>
                  <p>Low Stock Items</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon value">
                  <i className="fas fa-dollar-sign"></i>
                </div>
                <div className="stat-content">
                  <h3>
                    {formatCurrency(products.reduce((sum, p) => sum + (p.price * p.quantity), 0))}
                  </h3>
                  <p>Total Inventory Value</p>
                </div>
              </div>
            </div>

            <div className="overview-grid">
              <div className="card">
                <h3>Stock Alerts</h3>
                <div className="stock-alerts">
                  {outOfStockProducts.length > 0 && (
                    <div className="alert-section">
                      <h4 className="alert-title out-of-stock">
                        <i className="fas fa-times-circle"></i>
                        Out of Stock ({outOfStockProducts.length})
                      </h4>
                      {outOfStockProducts.map(product => (
                        <div key={product.id} className="alert-item">
                          <strong>{product.name}</strong>
                          <small>{product.sku}</small>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {lowStockProducts.filter(p => p.quantity > 0).length > 0 && (
                    <div className="alert-section">
                      <h4 className="alert-title low-stock">
                        <i className="fas fa-exclamation-triangle"></i>
                        Low Stock ({lowStockProducts.filter(p => p.quantity > 0).length})
                      </h4>
                      {lowStockProducts.filter(p => p.quantity > 0).map(product => (
                        <div key={product.id} className="alert-item">
                          <div>
                            <strong>{product.name}</strong>
                            <small>{product.sku}</small>
                          </div>
                          <span className="quantity-info">
                            {product.quantity} / {product.min_stock} min
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {outOfStockProducts.length === 0 && lowStockProducts.length === 0 && (
                    <div className="no-alerts">
                      <i className="fas fa-check-circle"></i>
                      <p>All products are well stocked!</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="card">
                <h3>Category Breakdown</h3>
                <div className="category-breakdown">
                  {categories.map(category => {
                    const categoryProducts = products.filter(p => p.category === category);
                    const totalValue = categoryProducts.reduce((sum, p) => sum + (p.price * p.quantity), 0);
                    return (
                      <div key={category} className="category-item">
                        <div className="category-info">
                          <strong>{category}</strong>
                          <small>{categoryProducts.length} products</small>
                        </div>
                        <div className="category-value">
                          {formatCurrency(totalValue)}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'products' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Product Inventory</h2>
              <div className="header-actions">
                <button 
                  className="btn btn-secondary"
                  onClick={() => setShowStockForm(true)}
                >
                  <i className="fas fa-exchange-alt"></i>
                  Stock Movement
                </button>
                <button 
                  className="btn btn-primary"
                  onClick={() => setShowProductForm(true)}
                >
                  <i className="fas fa-plus"></i>
                  Add Product
                </button>
              </div>
            </div>

            {showProductForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Add Product</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowProductForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleProductSubmit}>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Product Name</label>
                        <input
                          type="text"
                          className="form-control"
                          value={productForm.name}
                          onChange={(e) => setProductForm({...productForm, name: e.target.value})}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>SKU</label>
                        <input
                          type="text"
                          className="form-control"
                          value={productForm.sku}
                          onChange={(e) => setProductForm({...productForm, sku: e.target.value})}
                          required
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Category</label>
                        <input
                          type="text"
                          list="categories"
                          className="form-control"
                          value={productForm.category}
                          onChange={(e) => setProductForm({...productForm, category: e.target.value})}
                        />
                        <datalist id="categories">
                          {categories.map(cat => (
                            <option key={cat} value={cat} />
                          ))}
                        </datalist>
                      </div>
                      <div className="form-group">
                        <label>Price</label>
                        <input
                          type="number"
                          step="0.01"
                          className="form-control"
                          value={productForm.price}
                          onChange={(e) => setProductForm({...productForm, price: e.target.value})}
                          required
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Initial Quantity</label>
                        <input
                          type="number"
                          className="form-control"
                          value={productForm.quantity}
                          onChange={(e) => setProductForm({...productForm, quantity: e.target.value})}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>Minimum Stock Level</label>
                        <input
                          type="number"
                          className="form-control"
                          value={productForm.min_stock}
                          onChange={(e) => setProductForm({...productForm, min_stock: e.target.value})}
                          required
                        />
                      </div>
                    </div>
                    <div className="form-group">
                      <label>Description</label>
                      <textarea
                        className="form-control"
                        rows="3"
                        value={productForm.description}
                        onChange={(e) => setProductForm({...productForm, description: e.target.value})}
                      ></textarea>
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowProductForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Add Product
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            {showStockForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Record Stock Movement</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowStockForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleStockSubmit}>
                    <div className="form-group">
                      <label>Product</label>
                      <select
                        className="form-control"
                        value={stockForm.product_id}
                        onChange={(e) => setStockForm({...stockForm, product_id: e.target.value})}
                        required
                      >
                        <option value="">Select Product</option>
                        {products.map(product => (
                          <option key={product.id} value={product.id}>
                            {product.name} ({product.sku}) - Current: {product.quantity}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Type</label>
                        <select
                          className="form-control"
                          value={stockForm.type}
                          onChange={(e) => setStockForm({...stockForm, type: e.target.value})}
                        >
                          <option value="in">Stock In</option>
                          <option value="out">Stock Out</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Quantity</label>
                        <input
                          type="number"
                          className="form-control"
                          value={stockForm.quantity}
                          onChange={(e) => setStockForm({...stockForm, quantity: e.target.value})}
                          required
                        />
                      </div>
                    </div>
                    <div className="form-group">
                      <label>Reason</label>
                      <input
                        type="text"
                        className="form-control"
                        value={stockForm.reason}
                        onChange={(e) => setStockForm({...stockForm, reason: e.target.value})}
                        placeholder="e.g., Purchase, Sale, Damaged, etc."
                        required
                      />
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowStockForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Record Movement
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
                    <th>Product</th>
                    <th>SKU</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Min Stock</th>
                    <th>Status</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map(product => {
                    const stockStatus = getStockStatus(product);
                    return (
                      <tr key={product.id}>
                        <td>
                          <div>
                            <strong>{product.name}</strong>
                            {product.description && <br />}
                            <small>{product.description}</small>
                          </div>
                        </td>
                        <td>{product.sku}</td>
                        <td>{product.category}</td>
                        <td>{formatCurrency(product.price)}</td>
                        <td>
                          <span className={`quantity ${stockStatus}`}>
                            {product.quantity}
                          </span>
                        </td>
                        <td>{product.min_stock}</td>
                        <td>
                          <span className={`stock-status ${stockStatus}`}>
                            {getStockStatusLabel(stockStatus)}
                          </span>
                        </td>
                        <td>{formatCurrency(product.price * product.quantity)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Inventory;