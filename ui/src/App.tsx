import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ArticlesTable from "./ArticlesTable";
import Cards, { loader as CardsLoader} from "./Cards";
import React from "react";
import AddArticleForm from "./AddArticleForm";


function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <ArticlesTable></ArticlesTable>,
    },
    {
      path: "/:articleId/cards",
      element: <Cards></Cards>,
      loader: CardsLoader
    },
    {
      path: "/articles/add",
      element: <AddArticleForm></AddArticleForm>
    }
  ]);

  return (
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
  );
}

export default App;
