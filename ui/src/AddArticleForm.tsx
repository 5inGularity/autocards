import React, { useRef, useState } from "react";
import "./AddArticleForm.css"
import { useNavigate } from "react-router-dom";
import apiFetch from "./api";
import validator from 'validator';

function AddArticleForm() {
    const titleRef = useRef<HTMLInputElement>(null);
    const urlRef = useRef<HTMLInputElement>(null);
    const contentRef = useRef<HTMLTextAreaElement>(null);
    const [error, setError] = useState<string>();

    const navigate = useNavigate();

    const okHandler = async (event: React.MouseEvent) => {
        event.preventDefault();
        if (titleRef.current?.value === "") {
            setError("Title is required");
            titleRef.current?.focus();
            return;
        }
        if(urlRef.current?.value !== "" && !validator.isURL(urlRef.current?.value ?? "")) {
            setError("Invalid URL");
            urlRef.current?.focus();
            return;
        }
        const resp = await apiFetch("/articles/", {
            method: "POST",
            body: JSON.stringify({
                title: titleRef.current?.value ?? undefined,
                url: urlRef.current?.value ?? undefined,
                text: contentRef.current?.value ?? undefined
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        if (resp.status != 200) {
            setError(`Error adding article: ${resp.statusText}`)
        } else {
            navigate("/");
        }
    }

    const cancelHandler = (event: React.MouseEvent) => {
        event.preventDefault();
        navigate(-1);
    }

    return <div className="p-4 m-4">
        <h1 className="text-4xl">Add article</h1>
        <form className="flex flex-col">
            <div className="my-4 flex">
                <label htmlFor="titleInput" className="text-lg mx-4">Title</label>
                <input type="text" id="titleInput" placeholder="Enter title" ref={titleRef}></input>
            </div>
            <div className="border-2 border-gray-200 flex flex-col p-4">
                <div className="my-4 flex">
                    <label htmlFor="urlInput">URL</label>
                    <input type="text" id="urlInput" placeholder="Enter URL" ref={urlRef}></input>
                </div>
                <label className="text-center">OR</label>
                <div className="my-4 flex">
                    <label htmlFor="urlInput">Text content</label>
                    <textarea id="urlInput" placeholder="Enter text content" ref={contentRef}></textarea>
                </div>
            </div>
            {error && <div className="text-2xl m-4 text-red-400">{error}</div>}
            <div className="grow">
                <button onClick={okHandler}>Okay</button>
                <button onClick={cancelHandler}>Cancel</button>
            </div>
        </form>
    </div>
}

export default AddArticleForm;