import React, { useState, useEffect } from 'react';
import { hrAPI } from '../services/api';
import './HR.css';

const HR = ({ user }) => {
  const [activeTab, setActiveTab] = useState('employees');
  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showEmployeeForm, setShowEmployeeForm] = useState(false);
  const [showTaskForm, setShowTaskForm] = useState(false);

  const [employeeForm, setEmployeeForm] = useState({
    full_name: '',
    email: '',
    phone: '',
    role: '',
    department: '',
    salary: ''
  });

  const [taskForm, setTaskForm] = useState({
    title: '',
    description: '',
    assigned_to: '',
    priority: 'medium',
    due_date: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [employeesRes, tasksRes] = await Promise.all([
        hrAPI.getEmployees(),
        hrAPI.getTasks()
      ]);
      setEmployees(employeesRes.data);
      setTasks(tasksRes.data);
    } catch (error) {
      setError('Failed to load HR data');
      console.error('HR error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEmployeeSubmit = async (e) => {
    e.preventDefault();
    try {
      await hrAPI.addEmployee({
        ...employeeForm,
        salary: parseFloat(employeeForm.salary)
      });
      setEmployeeForm({
        full_name: '',
        email: '',
        phone: '',
        role: '',
        department: '',
        salary: ''
      });
      setShowEmployeeForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to add employee');
    }
  };

  const handleTaskSubmit = async (e) => {
    e.preventDefault();
    try {
      await hrAPI.createTask({
        ...taskForm,
        assigned_to: taskForm.assigned_to ? parseInt(taskForm.assigned_to) : null
      });
      setTaskForm({
        title: '',
        description: '',
        assigned_to: '',
        priority: 'medium',
        due_date: ''
      });
      setShowTaskForm(false);
      fetchData();
    } catch (error) {
      setError('Failed to create task');
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

  const getEmployeeName = (employeeId) => {
    const employee = employees.find(emp => emp.id === employeeId);
    return employee ? employee.full_name : 'Unassigned';
  };

  const tabs = [
    { id: 'employees', label: 'Employees', icon: 'fas fa-users' },
    { id: 'tasks', label: 'Tasks', icon: 'fas fa-tasks' },
    { id: 'overview', label: 'Overview', icon: 'fas fa-chart-bar' }
  ];

  const departments = [...new Set(employees.map(emp => emp.department).filter(Boolean))];
  const roles = [...new Set(employees.map(emp => emp.role).filter(Boolean))];

  return (
    <div className="main-content">
      <div className="hr-container">
        <div className="page-header">
          <h1>
            <i className="fas fa-users"></i>
            Human Resources
          </h1>
          <p>Manage employees, tasks, and HR operations</p>
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
            <div className="hr-stats">
              <div className="stat-card">
                <div className="stat-icon employees">
                  <i className="fas fa-users"></i>
                </div>
                <div className="stat-content">
                  <h3>{employees.filter(emp => emp.status === 'active').length}</h3>
                  <p>Active Employees</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon departments">
                  <i className="fas fa-building"></i>
                </div>
                <div className="stat-content">
                  <h3>{departments.length}</h3>
                  <p>Departments</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon tasks">
                  <i className="fas fa-tasks"></i>
                </div>
                <div className="stat-content">
                  <h3>{tasks.filter(task => task.status === 'pending').length}</h3>
                  <p>Pending Tasks</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon payroll">
                  <i className="fas fa-dollar-sign"></i>
                </div>
                <div className="stat-content">
                  <h3>
                    {formatCurrency(employees.reduce((sum, emp) => sum + (emp.salary || 0), 0))}
                  </h3>
                  <p>Total Payroll</p>
                </div>
              </div>
            </div>

            <div className="overview-grid">
              <div className="card">
                <h3>Department Distribution</h3>
                <div className="department-list">
                  {departments.map(dept => {
                    const count = employees.filter(emp => emp.department === dept).length;
                    return (
                      <div key={dept} className="department-item">
                        <span>{dept}</span>
                        <strong>{count} employees</strong>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="card">
                <h3>Recent Tasks</h3>
                <div className="recent-tasks">
                  {tasks.slice(0, 5).map(task => (
                    <div key={task.id} className="task-item">
                      <div className="task-info">
                        <strong>{task.title}</strong>
                        <small>Assigned to: {getEmployeeName(task.assigned_to)}</small>
                      </div>
                      <span className={`status-badge status-${task.status}`}>
                        {task.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'employees' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Employee Management</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowEmployeeForm(true)}
              >
                <i className="fas fa-plus"></i>
                Add Employee
              </button>
            </div>

            {showEmployeeForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Add Employee</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowEmployeeForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleEmployeeSubmit}>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Full Name</label>
                        <input
                          type="text"
                          className="form-control"
                          value={employeeForm.full_name}
                          onChange={(e) => setEmployeeForm({...employeeForm, full_name: e.target.value})}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>Email</label>
                        <input
                          type="email"
                          className="form-control"
                          value={employeeForm.email}
                          onChange={(e) => setEmployeeForm({...employeeForm, email: e.target.value})}
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Phone</label>
                        <input
                          type="tel"
                          className="form-control"
                          value={employeeForm.phone}
                          onChange={(e) => setEmployeeForm({...employeeForm, phone: e.target.value})}
                        />
                      </div>
                      <div className="form-group">
                        <label>Role</label>
                        <input
                          type="text"
                          className="form-control"
                          value={employeeForm.role}
                          onChange={(e) => setEmployeeForm({...employeeForm, role: e.target.value})}
                          required
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Department</label>
                        <input
                          type="text"
                          list="departments"
                          className="form-control"
                          value={employeeForm.department}
                          onChange={(e) => setEmployeeForm({...employeeForm, department: e.target.value})}
                        />
                        <datalist id="departments">
                          {departments.map(dept => (
                            <option key={dept} value={dept} />
                          ))}
                        </datalist>
                      </div>
                      <div className="form-group">
                        <label>Salary</label>
                        <input
                          type="number"
                          step="0.01"
                          className="form-control"
                          value={employeeForm.salary}
                          onChange={(e) => setEmployeeForm({...employeeForm, salary: e.target.value})}
                        />
                      </div>
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowEmployeeForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Add Employee
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
                    <th>Email</th>
                    <th>Role</th>
                    <th>Department</th>
                    <th>Salary</th>
                    <th>Hire Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.map(employee => (
                    <tr key={employee.id}>
                      <td>
                        <div>
                          <strong>{employee.full_name}</strong>
                          {employee.phone && <br />}
                          <small>{employee.phone}</small>
                        </div>
                      </td>
                      <td>{employee.email}</td>
                      <td>{employee.role}</td>
                      <td>{employee.department}</td>
                      <td>{employee.salary ? formatCurrency(employee.salary) : '-'}</td>
                      <td>{formatDate(employee.hire_date)}</td>
                      <td>
                        <span className={`status-badge status-${employee.status}`}>
                          {employee.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'tasks' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Task Management</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowTaskForm(true)}
              >
                <i className="fas fa-plus"></i>
                Create Task
              </button>
            </div>

            {showTaskForm && (
              <div className="modal-overlay">
                <div className="modal">
                  <div className="modal-header">
                    <h3>Create Task</h3>
                    <button 
                      className="close-btn"
                      onClick={() => setShowTaskForm(false)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                  <form onSubmit={handleTaskSubmit}>
                    <div className="form-group">
                      <label>Title</label>
                      <input
                        type="text"
                        className="form-control"
                        value={taskForm.title}
                        onChange={(e) => setTaskForm({...taskForm, title: e.target.value})}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Description</label>
                      <textarea
                        className="form-control"
                        rows="3"
                        value={taskForm.description}
                        onChange={(e) => setTaskForm({...taskForm, description: e.target.value})}
                      ></textarea>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Assign to Employee</label>
                        <select
                          className="form-control"
                          value={taskForm.assigned_to}
                          onChange={(e) => setTaskForm({...taskForm, assigned_to: e.target.value})}
                        >
                          <option value="">Select Employee</option>
                          {employees.filter(emp => emp.status === 'active').map(employee => (
                            <option key={employee.id} value={employee.id}>
                              {employee.full_name} - {employee.role}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Priority</label>
                        <select
                          className="form-control"
                          value={taskForm.priority}
                          onChange={(e) => setTaskForm({...taskForm, priority: e.target.value})}
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>
                    </div>
                    <div className="form-group">
                      <label>Due Date</label>
                      <input
                        type="date"
                        className="form-control"
                        value={taskForm.due_date}
                        onChange={(e) => setTaskForm({...taskForm, due_date: e.target.value})}
                      />
                    </div>
                    <div className="form-actions">
                      <button type="button" className="btn btn-secondary" onClick={() => setShowTaskForm(false)}>
                        Cancel
                      </button>
                      <button type="submit" className="btn btn-primary">
                        Create Task
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
                    <th>Title</th>
                    <th>Assigned To</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Due Date</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {tasks.map(task => (
                    <tr key={task.id}>
                      <td>
                        <div>
                          <strong>{task.title}</strong>
                          {task.description && <br />}
                          <small>{task.description}</small>
                        </div>
                      </td>
                      <td>{getEmployeeName(task.assigned_to)}</td>
                      <td>
                        <span className={`priority-badge priority-${task.priority}`}>
                          {task.priority}
                        </span>
                      </td>
                      <td>
                        <span className={`status-badge status-${task.status}`}>
                          {task.status}
                        </span>
                      </td>
                      <td>{task.due_date ? formatDate(task.due_date) : '-'}</td>
                      <td>{formatDate(task.created_at)}</td>
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

export default HR;