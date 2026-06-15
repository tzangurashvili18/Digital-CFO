import { useState } from "react";

const PASSCODE = "commschool782@cfo";

export default function Login({ onAuth }) {
  const [val, setVal] = useState("");
  const [err, setErr] = useState(false);

  const handleSubmit = () => {
    if (val === PASSCODE) {
      onAuth();
    } else {
      setErr(true);
      setVal("");
      setTimeout(() => setErr(false), 2000);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "#0f1117" }}>
      <div className="w-full max-w-sm">
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8">
          <div className="mb-8 text-center">
            <div className="text-xs font-semibold tracking-widest text-slate-500 uppercase mb-2">Commschool</div>
            <div className="text-2xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Digital <span style={{ color: "#6c63ff" }}>CFO</span>
            </div>
            <div className="text-slate-400 text-sm mt-2">Internal financial dashboard</div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
                Access Code
              </label>
              <input
                type="password"
                value={val}
                onChange={e => setVal(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleSubmit()}
                placeholder="Enter passcode"
                className={`w-full px-4 py-3 rounded-xl text-sm font-medium outline-none transition-all ${
                  err
                    ? "border-2 border-red-500 bg-red-900/10 text-red-300 placeholder-red-800"
                    : "border border-slate-600 bg-slate-700/50 text-white placeholder-slate-500 focus:border-violet-500"
                }`}
                style={{ fontFamily: "Space Grotesk, monospace" }}
                autoFocus
              />
              {err && (
                <p className="text-red-400 text-xs mt-2">Incorrect code. Try again.</p>
              )}
            </div>

            <button
              onClick={handleSubmit}
              className="w-full py-3 rounded-xl text-sm font-semibold transition-all"
              style={{ background: "#6c63ff", color: "white" }}
              onMouseEnter={e => e.target.style.background = "#5a52e8"}
              onMouseLeave={e => e.target.style.background = "#6c63ff"}
            >
              Enter
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
