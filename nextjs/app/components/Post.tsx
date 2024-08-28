'use client';
import { FormEvent, useState } from "react";

const Post = () => {
    const [data, setData] = useState('');

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            body: JSON.stringify({
                text: data
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
    }

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text"
                onChange={e => setData(e.target.value)} 
            />
            <button type="submit">Send</button>
        </form>
    );
}

export default Post