/**
 * views/dashboard.js — Dashboard tab
 */
import { state } from "../state.js";
import { fmt } from "../utils.js";

export function renderDashboard(el) {
    const plan = state.plan;
    if (!plan) {
        el.innerHTML = `<p class="text-slate-500 text-center py-20">Načítám plán…</p>`;
        return;
    }
    let rP=0,rC=0,rF=0, mP=0,mC=0,mF=0;
    const days = plan.days || [];
    days.forEach(d => {
        rP += d.macros_radim.protein_g;  rC += d.macros_radim.carbs_g;  rF += d.macros_radim.fat_g;
        mP += d.macros_monika.protein_g; mC += d.macros_monika.carbs_g; mF += d.macros_monika.fat_g;
    });
    const n = days.length || 1;
    const avg = v => Math.round(v / n);

    el.innerHTML = `
    <div class="space-y-10">
        <div class="glass p-12 bg-gradient-to-br from-emerald-950/40 via-slate-950 to-slate-950 shadow-2xl">
            <div class="flex flex-col xl:flex-row justify-between items-start gap-12">
                <div class="max-w-3xl">
                    <h1 class="text-5xl font-black mb-6 leading-none tracking-tight">
                        ${plan.name}<br>
                        <span class="text-emerald-400 underline decoration-emerald-800">7-denní plán</span>
                    </h1>
                    <p class="text-slate-400 text-xl">
                        Radime, cíl: 75 kg (~2100 kcal). Moniko, cíl: 60 kg (~1450 kcal).<br>
                        <span class="text-white font-bold italic">Vše váženo syrové. Tuky na vaření jsou započítány.</span>
                    </p>
                </div>
                <div class="grid grid-cols-2 gap-6 w-full xl:w-auto">
                    <div class="bg-emerald-500/5 p-8 rounded-[2.5rem] border border-emerald-500/20 text-center">
                        <p class="text-xs font-black uppercase text-emerald-400 mb-2 tracking-widest">Radim Target</p>
                        <p class="text-5xl font-black">2 100</p>
                        <p class="text-[10px] opacity-50 uppercase mt-2">kcal / den</p>
                    </div>
                    <div class="bg-rose-500/5 p-8 rounded-[2.5rem] border border-rose-500/20 text-center">
                        <p class="text-xs font-black uppercase text-rose-400 mb-2 tracking-widest">Monika Target</p>
                        <p class="text-5xl font-black">1 450</p>
                        <p class="text-[10px] opacity-50 uppercase mt-2">kcal / den</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass p-10">
                <h3 class="text-[10px] font-black uppercase text-slate-500 mb-8 tracking-[0.3em]">Týdenní predikce úbytku</h3>
                <div class="h-64 flex items-end justify-between px-10">
                    <div class="w-20 bg-emerald-500/20 rounded-t-2xl flex flex-col items-center p-4 h-[90%] border border-emerald-500/30">
                        <span class="text-xs font-black text-emerald-400">Radim</span>
                        <span class="text-xl font-black mt-auto">-0.8kg</span>
                    </div>
                    <div class="w-20 bg-rose-500/20 rounded-t-2xl flex flex-col items-center p-4 h-[70%] border border-rose-500/30">
                        <span class="text-xs font-black text-rose-400">Monika</span>
                        <span class="text-xl font-black mt-auto">-0.5kg</span>
                    </div>
                </div>
            </div>
            <div class="glass p-10 flex flex-col justify-center">
                <h3 class="text-[10px] font-black uppercase text-slate-500 mb-6 tracking-[0.3em]">Instrukce k vážení</h3>
                <ul class="space-y-4 text-sm text-slate-300">
                    <li class="flex gap-4 items-center bg-white/5 p-4 rounded-2xl"><span class="text-2xl">🥩</span><span><strong>Maso:</strong> Vždy važte syrové z balíčku.</span></li>
                    <li class="flex gap-4 items-center bg-white/5 p-4 rounded-2xl"><span class="text-2xl">🍚</span><span><strong>Přílohy:</strong> Rýži a čočku suchou, brambory syrové.</span></li>
                    <li class="flex gap-4 items-center bg-white/5 p-4 rounded-2xl"><span class="text-2xl">🥄</span><span><strong>Tuky:</strong> Olej v tabulkách je na celou přípravu.</span></li>
                </ul>
            </div>
        </div>
        <div class="glass p-10">
            <h3 class="text-[10px] font-black uppercase text-slate-500 mb-6 tracking-[0.3em]">Průměr / den — makra</h3>
            <div style="position:relative;height:260px;width:100%;"><canvas id="mainChart"></canvas></div>
        </div>
    </div>`;

    requestAnimationFrame(() => {
        const ctx = document.getElementById("mainChart")?.getContext("2d");
        if (!ctx || typeof Chart === "undefined") return;
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Bílkoviny (g)", "Sacharidy (g)", "Tuky (g)"],
                datasets: [
                    { label:"Radim",  data:[avg(rP),avg(rC),avg(rF)], backgroundColor:"#10b981", borderRadius:12 },
                    { label:"Monika", data:[avg(mP),avg(mC),avg(mF)], backgroundColor:"#fb7185", borderRadius:12 },
                ],
            },
            options: {
                responsive:true, maintainAspectRatio:false,
                scales: {
                    y:{ beginAtZero:true, grid:{color:"rgba(255,255,255,0.05)"}, ticks:{color:"#64748b"} },
                    x:{ grid:{display:false}, ticks:{color:"#64748b"} },
                },
                plugins:{ legend:{ labels:{ color:"#f1f5f9", font:{weight:"800"} } } },
            },
        });
    });
}
