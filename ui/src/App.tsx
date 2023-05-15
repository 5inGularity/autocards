import React, { useEffect, useState } from 'react';
import apiFetch from './api';

type Article = {
  id: number;
  title: string;
  url: string;
  status: string;
}

function App() {
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    const fetchArticles = async () => {
      const articlesResp = await apiFetch("/articles");
      const articles = await articlesResp.json() as unknown as Article[];
      console.log(articles);
      setArticles(articles);
    }
    fetchArticles();
  }, [])

  return (
    <table>
      <thead>
        <tr>
          <th>Url</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {articles.map(a => <tr key={a.id}>
          <td>{a.url}</td>
          <td>{a.status}</td>
        </tr>)}
      </tbody>
    </table>
  );
}

export default App;
