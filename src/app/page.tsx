'use client';

import { useChat } from 'ai/react';

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <main className="flex min-h-screen flex-col bg-gradient-to-b from-[#e3e0e7] to-[#babdf7] text-black">
      <div className="container flex flex-col gap-12 px-4 py-16 ">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          Build Your Profile
        </h1>
        <div className="mx-auto w-full max-w-md py-24 flex flex-col stretch">
          {messages.map(m => (
            <div key={m.id}>
              {m.role === 'user' ? 'User: ' : 'AI: '}
              {m.content}
            </div>
          ))}

          <form onSubmit={handleSubmit}>
            <label>
              Say something...
              <input
                className="fixed w-full max-w-md bottom-0 border border-gray-300 rounded mb-8 shadow-xl p-2"
                value={input}
                onChange={handleInputChange}
              />
            </label>
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </main>
  );
}
