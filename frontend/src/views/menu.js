/**
 * views/menu.js — 7-denní menu tab
 */
import { state } from "../state.js";
import { mealBlock, macroCard, bindLiveCalc } from "../components.js";

export function renderMenu(el) {
    const plan = state.plan;
    if (!plan) { el.innerHTML = `<p class="text-slate-500 text-center py-20">Načítám…</p>`; return; }

    el.innerHTML = (plan.days || []).map(day => `
    <div class="glass overflow-hidden mb-16 shadow-2xl">
        <div class="p-10 border-b border-white/5 flex flex-col xl:flex-row justify-between items-center gap-8 bg-white/5">
            <h2 class="text-4xl font-black text-white italic tracking-tighter uppercase">${day.day_name}</h2>
            <div class="flex gap-6">
                ${macroCard({
                    name:    "Radim",
                    kcal:    day.macros_radim.energy_kcal,
                    protein: day.macros_radim.protein_g,
                    carbs:   day.macros_radim.carbs_g,
                    fat:     day.macros_radim.fat_g,
                    target:  2100, color: "emerald",
                })}
                ${macroCard({
                    name:    "Monika",
                    kcal:    day.macros_monika.energy_kcal,
                    protein: day.macros_monika.protein_g,
                    carbs:   day.macros_monika.carbs_g,
                    fat:     day.macros_monika.fat_g,
                    target:  1450, color: "rose",
                })}
            </div>
        </div>
        <div class="p-10 space-y-20">
            ${day.meals.map(mealBlock).join("")}
        </div>
    </div>`).join("");

    // Připnout live přepočty na všechny inputy
    bindLiveCalc(el);
}
