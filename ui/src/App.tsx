import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ArticlesTable from "./ArticlesTable";
import Cards, { loader as CardsLoader} from "./Cards";
import React from "react";


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
  ]);

  return (
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
  );
}

export default App;
