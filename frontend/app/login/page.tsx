"use client";
import React, { FormEvent, useState } from 'react';
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "next/navigation";

export default function Login() {
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const router = useRouter();
  const setToken = useAuthStore((s) => s.setToken);

  
  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    console.log(formData.get("email"));
    console.log(formData.get("password"));
    setToken(email);
    router.push("/talk");
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-black text-white">

      <form
        onSubmit={handleLogin}
        className="w-full max-w-md p-8 rounded-2xl bg-zinc-900 border border-zinc-700 space-y-5"
      >
        <h1 className="text-xl font-semibold text-center">Login</h1>

        <input
          type="email"
          placeholder="Email"
          name = "email"
          className="w-full px-4 py-3 rounded-lg bg-zinc-800"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          name = "password"
          className="w-full px-4 py-3 rounded-lg bg-zinc-800"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="w-full py-3 rounded-lg bg-white text-black font-medium">
          Sign In
        </button>
      </form>

    </div>
  );
}
