import { useLoaderData } from "react-router-dom";
import apiFetch from "./api";
import { useState } from "react";


export async function loader({params} : any) {
    return apiFetch(`/articles/${params.articleId}/cards`)
}

type Card = {
    id: number;
    front: String;
    back: String;
}

export default function Cards() {
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const [backVisible, setBackVisible] = useState(false);
    const cards  = useLoaderData() as Card[];
    return <>
        {cards.length === 0 && <div className="text-xl4 p-4 text-center">Sorry, no cards for this article.</div>}
        {cards.length !== 0 && 
            <div className="flex flex-row h-screen">
                <div className={"basis-1/4 hover:bg-gray-200 text-8xl text-right align-middle p-4 " + (currentCardIndex > 0 ? "cursor-pointer" : "cursor-not-allowed")} onClick={() => {
                    if(currentCardIndex > 0) {
                        setBackVisible(false);
                        setCurrentCardIndex(currentCardIndex - 1);
                    }
                }}>
                    ⬅️
                </div>
                <div className="grow flex-col h-full pt-4 pb-4">
                    <div className="grow flex flex-col text-center border-spacing-10 border-4 rounded-xl border-gray-500 h-1/2 bg-gray-100">
                        <div className="grow cursor-pointer p-4" onClick={() => setBackVisible(true)}>
                            <span className="align-middle text-6xl" >{cards[currentCardIndex].front}</span>
                        </div>
                        <div className="text-right p-4">
                            {`${currentCardIndex+1}/${cards.length}`}
                        </div>
                    </div>
                    {backVisible && <div className="grow text-center h-1/2 text-4xl">{cards[currentCardIndex].back}</div>}
                </div>
                <div className={"basis-1/4 hover:bg-gray-200 text-8xl text-left align-middle p-4 " + (currentCardIndex < cards.length - 1 ? "cursor-pointer" : "cursor-not-allowed")} onClick={() => {
                    if(currentCardIndex < cards.length - 1) {
                        setBackVisible(false);
                        setCurrentCardIndex(currentCardIndex + 1);
                    }
                }}>
                    ➡️
                </div>
                
            </div>
        }
    </>
}