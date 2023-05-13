import React, { useState, useEffect } from 'react';

interface Data {
  id: number;
  name: string;
  description: string;
}

function App() {
  const [data, setData] = useState<Data[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await fetch('/db');
      const data = await result.json();
      setData(data);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Example App</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
