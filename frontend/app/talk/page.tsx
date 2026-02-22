"use client";

import { useRef, useState } from "react";
import { Mic, ImagePlus, Search, Loader2 } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8080";

export default function TV() {
  const { token: userId } = useAuthStore();

  const searchRef = useRef<HTMLInputElement | null>(null);

  const [image,        setImage]        = useState<string | null>(null);
  const [currentFile,  setCurrentFile]  = useState<File | null>(null);
  const [conversation, setConversation] = useState("");
  const [answer,       setAnswer]       = useState<string | null>(null);
  const [loading,      setLoading]      = useState(false);
  const [error,        setError]        = useState<string | null>(null);

  async function handleSave() {
    if (!currentFile || !userId) return;

    const combinedConversation = [answer, conversation].filter(Boolean).join(" — ");

    setError(null);
    setLoading(true);

    const form = new FormData();
    form.append("file", currentFile);

    try {
      const res = await fetch(
        `${BACKEND_URL}/upload/${encodeURIComponent(userId)}?conversation=${encodeURIComponent(combinedConversation)}`,
        { method: "POST", body: form }
      );
      if (!res.ok) throw new Error(`Upload failed (${res.status})`);
      setConversation("");
      setImage(null);
      setCurrentFile(null);
      setAnswer(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !userId) return;

    setCurrentFile(file);
    setImage(URL.createObjectURL(file));
    setAnswer(null);
    setError(null);
    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(
        `${BACKEND_URL}/search/${encodeURIComponent(userId)}`,
        { method: "POST", body: form }
      );
      if (!res.ok) throw new Error(`Search failed (${res.status})`);
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setLoading(false);
      if (searchRef.current) searchRef.current.value = "";
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center px-4 pb-40 pt-10">

      {/* TV FRAME */}
      <div className="w-full max-w-md rounded-2xl border border-zinc-700/50 bg-zinc-900 shadow-[0_0_60px_rgba(0,0,0,0.8)] overflow-hidden">

        {/* SCREEN */}
        <div className="relative bg-black flex items-center justify-center">

          {image ? (
            <img
              src={image}
              className="w-full h-auto max-h-[60vh] object-contain block"
            />
          ) : (
            <div className="h-56 flex flex-col items-center justify-center gap-3 text-zinc-600">
              <Search size={28} strokeWidth={1.5} />
              <p className="text-xs tracking-wide uppercase">Tap "Who is this?" to begin</p>
            </div>
          )}

          {/* Loading overlay */}
          {loading && (
            <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
              <Loader2 className="animate-spin text-white/80" size={36} />
            </div>
          )}

          {/* Answer subtitle */}
          {answer && !loading && (
            <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/90 to-transparent px-5 pt-8 pb-4">
              <p className="text-white/90 text-sm leading-relaxed">{answer}</p>
            </div>
          )}

          {/* Error bar */}
          {error && !loading && (
            <div className="absolute bottom-0 inset-x-0 bg-red-950/90 px-5 py-3">
              <p className="text-red-300 text-xs">{error}</p>
            </div>
          )}

        </div>
      </div>

      {/* CONTROLS — fixed to bottom */}
      <div className="fixed bottom-6 left-0 right-0 bg-zinc-950/95 backdrop-blur-md border-t border-zinc-800/60 px-4 py-4">
        <div className="max-w-md mx-auto space-y-3">

          <input
            type="text"
            value={conversation}
            onChange={(e) => setConversation(e.target.value)}
            placeholder="Add a note about this memory…"
            className="w-full bg-zinc-800/80 text-zinc-100 placeholder-zinc-600 rounded-xl px-4 py-2.5 text-sm outline-none focus:ring-1 focus:ring-zinc-500 transition"
          />

          <div className="flex gap-2">

            <button
              onClick={handleSave}
              disabled={loading || !currentFile}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm transition disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ImagePlus size={16} />
              Save
            </button>

            <button
              onClick={() => searchRef.current?.click()}
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-white text-black text-sm font-medium hover:bg-zinc-100 transition disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <Search size={16} />
              Who is this?
            </button>

            <button
              className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm transition"
            >
              <Mic size={16} />
            </button>

          </div>
        </div>
      </div>

      <input type="file" accept="image/*" hidden ref={searchRef} onChange={handleSearch} />

    </div>
  );
}
