import { useEffect, useState } from 'react';
import apiFetch from './api';
import validator from 'validator';
import { useNavigate } from 'react-router-dom';


type Article = {
  id: number;
  title: string;
  url: string;
  status: string;
}

function ArticlesTable() {
  const [articles, setArticles] = useState<Article[]>([]);

  const navigate = useNavigate();

  const fetchArticles = async () => {
    const articlesResp = await apiFetch("/articles");
    const articles = await articlesResp.json() as unknown as Article[];
   
    setArticles(articles);
  }
  useEffect(() => {
    fetchArticles();
  }, [])

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchArticles();
    }, 5000);

    // Clean up the interval on component unmount
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const deleteArticle = async(articleId: number) => {
    const resp = await apiFetch("/articles/" + articleId, {
        method: "DELETE",
        headers: {
            "Content-type" : "application/json"
        }
    })
    if(resp.status !== 200) {
        console.log(resp.text);
    } else {
        fetchArticles();
    }
  }

  return (
    <>
        <div className='p-4 flex flex-row w-full'>
            <div className='text-4xl grow content-start' >Articles</div>
            <div className='text-right content-end align-text-bottom px-4 grow'>
                <button className='bg-gray-200 border-gray-500 border-2 px-4 py-2 disabled:bg-gray-50' onClick={() => {
                    navigate("/articles/add");
                }}>Add</button>
            </div>
        </div>
        <table className='table-auto w-full text-left text-sm text-gray-500'>
            <thead className='text-xs text-gray-700 bg-gray-50 border-2'>
                <tr>
                <th scope="col" className='px-6 py-3'>Title</th>
                <th scope="col" className='px-6 py-3'>Status</th>
                <th scope="col" className='px-6 py-3'></th>
                </tr>
            </thead>
            <tbody>
                {articles.map(a => <tr key={a.id} className='bg-white border-b'>
                <td className='px-6 py-4 flex-wrap'>{a.title}</td>
                <td className='px-6 py-4'>{a.status}</td>
                <td className='text-4xl px-6 py-4'>{a.status === "ready" && <a href={`${a.id}/cards`}>▶️</a>}</td>
                <td className='text-4xl px-6 py-4'><span className='cursor-pointer' onClick={() => deleteArticle(a.id)}>🗑️</span></td>
                </tr>)}
            </tbody>
        </table>
    </>
  );
}

export default ArticlesTable;
