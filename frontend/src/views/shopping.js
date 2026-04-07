/**
 * views/shopping.js — Nákupní seznam tab
 */
import { state } from "../state.js";
import { fmtG } from "../utils.js";

const CAT_LABELS = {
    maso_drubez:   "Drůbež",
    maso_hovezi:   "Hovězí",
    maso_veprove:  "Vepřové",
    maso_ryby:     "Ryby",
    mlecne_vyrobky:"Mléčné",
    vejce:         "Vejce",
    obili_pecivo:  "Obiloviny",
    lustediny:     "Luštěniny",
    zelenina:      "Zelenina",
    ovoce:         "Ovoce",
    tuky_oleje:    "Tuky",
    orechy_seminka:"Ořechy",
    ostatni:       "Ostatní",
};

export function renderShopping(el) {
    const s = state.shopping;
    if (!s) { el.innerHTML = `<p class="text-slate-500 text-center py-20">Načítám…</p>`; return; }

    const rows = s.items.map(item => `
    <tr class="hover:bg-white/5 transition-colors">
        <td class="p-6 text-[10px] font-black text-slate-500 uppercase tracking-tighter">
            ${CAT_LABELS[item.category] || item.category || "—"}
        </td>
        <td class="p-6 font-bold text-white text-sm">${item.name}</td>
        <td class="p-6 text-slate-400 text-sm font-bold">${fmtG(item.total_g)}</td>
        <td class="p-6 text-right font-black text-emerald-400 text-lg">${item.estimated_czk} Kč</td>
    </tr>`).join("");

    el.innerHTML = `
    <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-8">
        <div>
            <h2 class="text-4xl font-black">Kompletní Nákup</h2>
            <p class="text-slate-500 text-lg">Sumář surovin pro celý týden.</p>
        </div>
        <div class="bg-emerald-500/10 p-8 rounded-[2.5rem] border border-emerald-500/20 text-right w-full md:w-auto">
            <p class="text-xs font-black text-emerald-400 uppercase mb-2">Odhad celkem</p>
            <p class="text-5xl font-black text-white">${s.estimated_czk} Kč</p>
        </div>
    </div>
    <div class="glass overflow-hidden shadow-2xl">
        <table class="w-full text-left text-sm">
            <thead class="bg-white/5 text-[10px] uppercase font-black text-slate-500">
                <tr>
                    <th class="p-6">Kategorie</th>
                    <th class="p-6">Surovina</th>
                    <th class="p-6">Množství</th>
                    <th class="p-6 text-right">Odhad Kč</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-white/5">${rows}</tbody>
        </table>
    </div>`;
}
