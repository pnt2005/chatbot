'use client';
import Pusher from 'pusher-js';
import { useState, useEffect } from 'react';
import Post from "./Post";

export default function Chat() {
  const [messages, setMessages] = useState<string[]>([]);
  Pusher.logToConsole = true;
  var pusher = new Pusher('b342d32dd9ff16552098', {
    cluster: 'ap1'
  });

  useEffect(() => {
    var question: any = document.getElementById("input");
    

    var channel = pusher.subscribe('my-channel');
    channel.unbind('my-event');
    channel.bind('my-event', function(data: any) {
      setMessages((prev) => [...prev, question.value]);
      setMessages((prev) => [...prev, data['message']]);
    });
    return () => pusher.unsubscribe('mychannel');
  }, []);

  return (
    <ul>
      {messages.map((text, index) => ( 
        <li key={index}>
          {text}
        </li>
      ))}
    </ul>
  );
}