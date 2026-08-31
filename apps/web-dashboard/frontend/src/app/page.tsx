"use client";

import React, { useState } from "react";
import { 
  FileSpreadsheet, 
  BarChart3, 
  ShieldCheck, 
  GitCompare, 
  Wrench, 
  UploadCloud, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle,
  Activity,
  Layers,
  Sparkles
} from "lucide-react";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "dcma" | "compare" | "tools">("overview");
  const [scheduleData, setScheduleData] = useState<any>({
    projectName: "Sample Hospital Construction",
    taskCount: 142,
    criticalCount: 18,
    relationshipCount: 284,
    healthScore: 92.8,
    status: "Active"
  });

  const dcmaChecks = [
    { id: 1, name: "Logic (Missing Pred/Succ)", threshold: "<= 5%", actual: "1.4%", status: "PASS" },
    { id: 2, name: "Leads (Negative Lags)", threshold: "0%", actual: "0.0%", status: "PASS" },
    { id: 3, name: "Lags (Positive Lags > 0)", threshold: "<= 5%", actual: "3.2%", status: "PASS" },
    { id: 4, name: "Relationship Types (FS %)", threshold: ">= 90%", actual: "94.5%", status: "PASS" },
    { id: 5, name: "Hard Constraints", threshold: "<= 5%", actual: "2.1%", status: "PASS" },
    { id: 6, name: "High Total Float (> 44d)", threshold: "<= 5%", actual: "4.8%", status: "PASS" },
    { id: 7, name: "Negative Total Float", threshold: "0%", actual: "0.0%", status: "PASS" },
    { id: 8, name: "High Duration (> 44d)", threshold: "<= 5%", actual: "6.1%", status: "FAIL" },
    { id: 9, name: "Invalid Dates Integrity", threshold: "0%", actual: "0.0%", status: "PASS" },
    { id: 10, name: "Resource Assignment Loading", threshold: ">= 90%", actual: "98.0%", status: "PASS" },
    { id: 11, name: "Missed Tasks (Finish vs BL)", threshold: "<= 5%", actual: "0.0%", status: "PASS" },
    { id: 12, name: "Critical Path Integrity Test", threshold: "Continuous", actual: "Connected", status: "PASS" },
    { id: 13, name: "Critical Path Float Index (CAPI)", threshold: "0.95-1.05", actual: "1.00", status: "PASS" },
    { id: 14, name: "Baseline Execution Index (BEI)", threshold: ">= 0.95", actual: "0.98", status: "PASS" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="bg-emerald-500/10 p-2 rounded-xl border border-emerald-500/20 text-emerald-400 font-bold flex items-center gap-2">
            <Layers className="w-5 h-5" />
            <span className="text-lg tracking-wide">PlanBee</span>
          </div>
          <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full border border-slate-700">v1.0.0 Open Source</span>
        </div>

        <nav className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
          <button 
            onClick={() => setActiveTab("overview")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition ${activeTab === "overview" ? "bg-slate-800 text-white" : "text-slate-400 hover:text-slate-200"}`}
          >
            <Activity className="w-4 h-4" /> Overview
          </button>
          <button 
            onClick={() => setActiveTab("dcma")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition ${activeTab === "dcma" ? "bg-slate-800 text-white" : "text-slate-400 hover:text-slate-200"}`}
          >
            <ShieldCheck className="w-4 h-4" /> DCMA 14-Point
          </button>
          <button 
            onClick={() => setActiveTab("compare")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition ${activeTab === "compare" ? "bg-slate-800 text-white" : "text-slate-400 hover:text-slate-200"}`}
          >
            <GitCompare className="w-4 h-4" /> Comparison
          </button>
          <button 
            onClick={() => setActiveTab("tools")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition ${activeTab === "tools" ? "bg-slate-800 text-white" : "text-slate-400 hover:text-slate-200"}`}
          >
            <Wrench className="w-4 h-4" /> CPM Tools
          </button>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {/* Upload Banner */}
        <div className="border-2 border-dashed border-slate-800 hover:border-emerald-500/50 transition rounded-2xl p-8 bg-slate-900/30 flex flex-col items-center justify-center text-center group cursor-pointer">
          <UploadCloud className="w-12 h-12 text-slate-500 group-hover:text-emerald-400 transition mb-3" />
          <h3 className="text-base font-semibold text-slate-200">Drag & Drop Primavera P6 (.XER) File</h3>
          <p className="text-xs text-slate-400 mt-1">Instant local parsing for DCMA 14-point audit, S-Curve generation, and CPM optimization</p>
        </div>

        {/* Tab 1: Overview */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <span className="text-xs text-slate-400 font-medium">Total Activities</span>
                <div className="text-2xl font-bold text-slate-100 mt-1">{scheduleData.taskCount}</div>
                <div className="text-xs text-emerald-400 mt-2 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> 100% Loaded
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <span className="text-xs text-slate-400 font-medium">Critical Path Tasks</span>
                <div className="text-2xl font-bold text-amber-400 mt-1">{scheduleData.criticalCount}</div>
                <div className="text-xs text-slate-400 mt-2">12.6% of project duration</div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <span className="text-xs text-slate-400 font-medium">Logic Relationships</span>
                <div className="text-2xl font-bold text-slate-100 mt-1">{scheduleData.relationshipCount}</div>
                <div className="text-xs text-emerald-400 mt-2">2.0 ties per task</div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <span className="text-xs text-slate-400 font-medium">DCMA Health Score</span>
                <div className="text-2xl font-bold text-emerald-400 mt-1">{scheduleData.healthScore}%</div>
                <div className="text-xs text-emerald-400 mt-2">13 / 14 Checks Passed</div>
              </div>
            </div>

            {/* S-Curve & Progress Box */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-base font-semibold text-slate-200">S-Curve Progress Baseline (PV vs EV vs AC)</h3>
                  <p className="text-xs text-slate-400">Cumulative physical percentage complete and earned value distribution</p>
                </div>
                <button className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1.5 rounded-lg hover:bg-emerald-500/20 transition">
                  Export Excel S-Curve
                </button>
              </div>
              <div className="h-64 border border-slate-800 rounded-lg flex items-center justify-center text-slate-500 bg-slate-950/50">
                <BarChart3 className="w-8 h-8 mr-2 text-slate-600" />
                <span>Interactive Chart Ready</span>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: DCMA 14-Point */}
        {activeTab === "dcma" && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-200">DCMA 14-Point Schedule Assessment</h3>
                <p className="text-xs text-slate-400">Standard Department of Defense schedule integrity metrics</p>
              </div>
              <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-4 py-2 rounded-xl text-sm font-semibold">
                <ShieldCheck className="w-5 h-5" /> 92.8% Health Score
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
              {dcmaChecks.map((chk) => (
                <div key={chk.id} className="border border-slate-800 bg-slate-950/50 rounded-lg p-4 flex items-center justify-between">
                  <div className="space-y-1">
                    <span className="text-sm font-medium text-slate-200">{chk.name}</span>
                    <div className="text-xs text-slate-400">Threshold: {chk.threshold} | Actual: <span className="font-semibold text-slate-300">{chk.actual}</span></div>
                  </div>
                  <span className={`text-xs px-2.5 py-1 rounded-md font-semibold ${chk.status === "PASS" ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" : "bg-rose-500/10 text-rose-400 border border-rose-500/20"}`}>
                    {chk.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 3: Comparison */}
        {activeTab === "compare" && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-lg font-semibold text-slate-200">Schedule Comparison (Claim Digger)</h3>
            <p className="text-xs text-slate-400">Compare Baseline schedule against Update schedule to detect scope, logic, and date variations</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
              <div className="border border-slate-800 rounded-xl p-6 bg-slate-950/50 text-center">
                <FileSpreadsheet className="w-8 h-8 mx-auto text-blue-400 mb-2" />
                <span className="text-sm font-medium text-slate-300">Baseline Schedule (.XER)</span>
              </div>
              <div className="border border-slate-800 rounded-xl p-6 bg-slate-950/50 text-center">
                <FileSpreadsheet className="w-8 h-8 mx-auto text-emerald-400 mb-2" />
                <span className="text-sm font-medium text-slate-300">Update Schedule (.XER)</span>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: Tools */}
        {activeTab === "tools" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <h4 className="font-semibold text-slate-200 text-sm">Redundant Logic Cleaner</h4>
              <p className="text-xs text-slate-400">Uses CPM transitive reduction to detect and eliminate duplicate logic ties.</p>
              <button className="w-full text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 py-2 rounded-lg transition font-medium">
                Run Logic Cleaner
              </button>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <h4 className="font-semibold text-slate-200 text-sm">Update Zeroing</h4>
              <p className="text-xs text-slate-400">Clears actuals and restores remaining durations to convert an update to a clean baseline.</p>
              <button className="w-full text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 py-2 rounded-lg transition font-medium">
                Zero Out Update
              </button>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <h4 className="font-semibold text-slate-200 text-sm">Excel &lt;-&gt; XER Converter</h4>
              <p className="text-xs text-slate-400">Bi-directional conversion between multi-tab Excel sheets and Primavera P6 XER.</p>
              <button className="w-full text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 py-2 rounded-lg transition font-medium">
                Convert Workbook
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
