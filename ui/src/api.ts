const host = window.location.hostname;
const protocol = window.location.protocol;
const BASE_URL = `${protocol}//${host}:8000`

const apiFetch = (url: string, options?: RequestInit): Promise<Response> => {
  const fullUrl = `${BASE_URL}${url}`;
  return fetch(fullUrl, options);
};

export default apiFetch;
