import { useState, useEffect } from 'react';
import { login, logout, fetchCurrentTask, fetchStats, updateTaskStatus, reSeedTasks, startSession } from './api';
import './App.css';
import LoginScreen from './components/LoginScreen';
import Header from './components/Header';
import CurrentItem from './components/CurrentItem';
import ComparisonPanel from './components/ComparisonPanel';
import ActionButtons from './components/ActionButtons';
import ProblemOverlay from './components/ProblemOverlay';

function App() {
  const [stats, setStats] = useState(null);
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [showProblemOverlay, setShowProblemOverlay] = useState(false);

  const loadData = async () => {
    try {
      const [statsData, taskData] = await Promise.all([fetchStats(), fetchCurrentTask()]);
      setStats(statsData.stats);
      setTask(taskData.task);
      setError(null);
      setLoading(false);

      if (!taskData.task) {
        await reSeedTasks();
        const [newStats, newTask] = await Promise.all([fetchStats(), fetchCurrentTask()]);
        setStats(newStats.stats);
        setTask(newTask.task);
      }
    } catch (err) {
      if (err.response && err.response.status === 403) {
        setIsAuthenticated(false);
        setLoading(false);
      }
      console.error("Error fetching kiosk data:", err);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadData();
      const interval = setInterval(loadData, 5000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated && isDemoMode && task && !showProblemOverlay) {
      const timer = setTimeout(() => {
        const randomAction = Math.random();
        let actionToTake = 'picked';

        if (randomAction < 0.70) actionToTake = 'picked';
        else if (randomAction < 0.80) actionToTake = 'unscannable';
        else if (randomAction < 0.90) actionToTake = 'missing';
        else actionToTake = 'problem_tote';

        handleAction(actionToTake);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, isDemoMode, task, showProblemOverlay]);

  const handleLogin = async (username, password) => {
    try {
      await login(username, password);
      await startSession();
      setIsAuthenticated(true);
      setLoading(false);
      loadData();
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  const handleLogout = async () => {
    await logout();
    setIsAuthenticated(false);
    setTask(null);
    setStats(null);
    setLoading(true);
    setIsDemoMode(false);
    setShowProblemOverlay(false);
  };

  const handleAction = async (newStatus) => {
    if (!task) return;
    try {
      await updateTaskStatus(task.id, newStatus);
      setTask({ ...task, status: newStatus });

      if (newStatus === 'picked') {
        await loadData();
      } else {
        setShowProblemOverlay(true);
      }
    } catch (err) {
      console.error("Failed to update task:", err);
      setError("Failed to update item. Please try again.");
    }
  };

  if (!isAuthenticated) {
    return <LoginScreen onLogin={handleLogin} error={error} />;
  }

  if (loading) return <div className="kiosk-loading">Loading Kiosk...</div>;

  return (
    <div className="kiosk">
      <Header stationId = "PickstationASRS4159" operatorName ={stats?.opearor_name} stats ={stats}/>
      <div className="demo-toggle">
        <label>
          <input 
            type="checkbox" 
            checked={isDemoMode} 
            onChange={(e) => setIsDemoMode(e.target.checked)} 
          />
          <strong> Demo Mode (Random Actions every 3 seconds)</strong>
        </label>
      </div>

      <main className="kiosk-main">
        <CurrentItem task={task} />
        <ComparisonPanel task={task} />
        {error && <div className="error-message">{error}</div>}
      </main>

      {showProblemOverlay && (
        <ProblemOverlay 
          task={task} 
          onResume={() => {
            setShowProblemOverlay(false);
            loadData();
          }} 
        />
      )}

      <ActionButtons onAction={handleAction} />

      <nav className="kiosk-nav">
        <button onClick={handleLogout}>Sign out</button>
        <button>Menu</button>
        <span className="clock">{new Date().toLocaleTimeString()}</span>
        <button>Andon</button>
        <button>Safety</button>
      </nav>
    </div>
  );
}

export default App;