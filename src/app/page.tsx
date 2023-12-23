import Link from "next/link";

import { CreatePost } from "~/app/_components/create-post";
import { api } from "~/trpc/server";

export default async function Home() {

  return (
    <main className="flex min-h-screen flex-col bg-gradient-to-b from-[#e3e0e7] to-[#babdf7] text-black">
      <div className="container flex flex-col gap-12 px-4 py-16 ">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          Build Your Profile
        </h1>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-8">
          <p>Instructions go here</p>
        </div>
        <input
          type="text"
          className="block flex-1 py-1.5 pl-1 focus:ring-0 sm:text-sm sm:leading-6"
        />
      </div>
    </main>
  );
}
