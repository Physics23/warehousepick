import axios from 'axios';

//const API_BASE_URL = 'http://127.0.0.1:8000/api';
//const STATION_ID = 'ToteASRS4159';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
const STATION_ID = 'ToteASRS4159';

axios.defaults.withCredentials = true;

export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login/`, { username, password });
  return response.data;
};

export const logout = async () => {
  const response = await axios.post(`${API_BASE_URL}/auth/logout/`, { station_id: STATION_ID });
  return response.data;
};

export const fetchCurrentTask = async () => {
  const response = await axios.get(`${API_BASE_URL}/stations/${STATION_ID}/current-task/`);
  return response.data;
};

export const fetchStats = async () => {
  const response = await axios.get(`${API_BASE_URL}/stations/${STATION_ID}/stats/`);
  return response.data;
};

export const updateTaskStatus = async (taskId, status) => {
  const response = await axios.patch(`${API_BASE_URL}/tasks/${taskId}/update_status/`, { status });
  return response.data;
};

export const reSeedTasks = async () => {
  const response = await axios.post(`${API_BASE_URL}/tasks/re-seed/`);
  return response.data;
};

export const startSession = async () => {
  const response = await axios.post(`${API_BASE_URL}/sessions/start/`);
  return response.data;
};

export const createItemWithImage = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/items/upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};