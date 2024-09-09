'use client';
import { FormEvent, useState } from "react";
    
export default function Post() {
    const [message, setMessage] = useState<string>("");

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            body: JSON.stringify({
                text: message
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        setMessage("");
    }

    return (
        <>
            <form onSubmit={handleSubmit}>
                <input 
                    id = "input"
                    type="text"
                    placeholder="type here"
                    value={message}
                    onChange={e => setMessage(e.target.value)} 
                />
                <button type="submit">Send</button>
            </form>
        </>
    );
}
