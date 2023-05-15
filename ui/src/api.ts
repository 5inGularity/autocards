const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiFetch = (url: string, options?: RequestInit): Promise<Response> => {
  const fullUrl = `${BASE_URL}${url}`;
  return fetch(fullUrl, options);
};

export default apiFetch;
