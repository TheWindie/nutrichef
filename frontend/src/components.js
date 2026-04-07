/**
 * components.js — HTML generátory pro opakující se UI bloky
 */
import { fmt, fmtG, MEAL_LABELS } from "./utils.js";

/** Karta s makry pro jednoho uživatele */
export function macroCard({ name, kcal, protein, carbs, fat, target, color }) {
    const pct = target > 0 ? Math.min(100, Math.round(kcal / target * 100)) : 0;
    const over = kcal > target * 1.1;
    return `
    <div class="bg-${color}-500/10 p-6 rounded-3xl border border-${color}-500/20 w-full shadow-inner">
        <p class="text-[9px] font-black uppercase text-${color}-400 mb-1 tracking-widest">${name}</p>
        <p class="text-3xl font-black text-white ${over ? "text-red-400" : ""}">${Math.round(kcal)} kcal</p>
        <p class="text-[9px] text-${color}-400/70 font-bold mt-1">
            B:${fmt(protein,1)}g &nbsp;S:${fmt(carbs,1)}g &nbsp;T:${fmt(fat,1)}g
        </p>
        <div class="mt-3 h-1.5 rounded-full bg-white/10 overflow-hidden">
            <div class="h-full bg-${color}-400 rounded-full transition-all"
                 style="width:${pct}%"></div>
        </div>
        <p class="text-[9px] text-${color}-400/50 mt-1">${pct}% denního cíle</p>
    </div>`;
}

/** Řádek tabulky s ingrediencí */
export function ingredientRow(ing) {
    const mr = ing.macros_radim  || {};
    const mm = ing.macros_monika || {};
    return `
    <tr class="border-b border-white/5 text-[11px] hover:bg-white/5 transition-colors group">
        <td class="py-4 font-bold text-slate-300 group-hover:text-white sticky-col">${ing.food_name}</td>
        <td class="py-4 text-center text-emerald-400 font-black">${ing.amount_radim_g}g</td>
        <td class="py-4 text-center text-emerald-100">${fmt(mr.energy_kcal)}</td>
        <td class="py-4 text-center text-emerald-100">${fmt(mr.protein_g,1)}</td>
        <td class="py-4 text-center text-emerald-100">${fmt(mr.carbs_g,1)}</td>
        <td class="py-4 text-center text-emerald-100">${fmt(mr.fat_g,1)}</td>
        <td class="py-4 text-center text-rose-400 font-black border-l border-white/10">${ing.amount_monika_g}g</td>
        <td class="py-4 text-center text-rose-100">${fmt(mm.energy_kcal)}</td>
        <td class="py-4 text-center text-rose-100">${fmt(mm.protein_g,1)}</td>
        <td class="py-4 text-center text-rose-100">${fmt(mm.carbs_g,1)}</td>
        <td class="py-4 text-center text-rose-100">${fmt(mm.fat_g,1)}</td>
    </tr>`;
}

/** Hlavička tabulky ingrediencí */
export const ingredientTableHead = `
<thead class="bg-white/5 text-[9px] uppercase font-black text-slate-500">
    <tr>
        <th class="p-4 sticky-col">Surovina (syrová)</th>
        <th class="p-4 text-center text-emerald-400">R (g)</th>
        <th class="p-4 text-center">kcal</th><th class="p-4 text-center">B</th>
        <th class="p-4 text-center">S</th><th class="p-4 text-center">T</th>
        <th class="p-4 text-center text-rose-400 border-l border-white/10">M (g)</th>
        <th class="p-4 text-center">kcal</th><th class="p-4 text-center">B</th>
        <th class="p-4 text-center">S</th><th class="p-4 text-center">T</th>
    </tr>
</thead>`;

/** Blok jednoho jídla (snídaně/oběd/večeře) */
export function mealBlock(meal) {
    const rows = meal.ingredients.map(ingredientRow).join("");
    const mr = meal.macros_radim  || {};
    const mm = meal.macros_monika || {};
    return `
    <div class="space-y-6">
        <div class="flex flex-col md:flex-row md:items-center gap-4">
            <span class="text-[10px] font-black uppercase bg-emerald-500/20 text-emerald-400
                         px-4 py-2 rounded-2xl border border-emerald-500/20 w-fit">
                ${MEAL_LABELS[meal.meal_type] || meal.meal_type}
            </span>
            <h4 class="text-2xl font-black text-white tracking-tight leading-none">${meal.name}</h4>
        </div>
        <div class="overflow-x-auto rounded-[1.5rem] border border-white/5 shadow-2xl">
            <table class="w-full text-left min-w-[1000px]">
                ${ingredientTableHead}
                <tbody>${rows}</tbody>
                <tfoot class="bg-white/10 font-black text-[12px] text-white">
                    <tr>
                        <td class="p-5 px-6 uppercase tracking-widest text-[10px] sticky-col">SOUČET</td>
                        <td colspan="5" class="p-5 text-center text-emerald-400 underline decoration-2 decoration-emerald-800">
                            ${Math.round(mr.energy_kcal || 0)} kcal
                        </td>
                        <td colspan="5" class="p-5 text-center text-rose-400 border-l border-white/10 underline decoration-2 decoration-rose-800">
                            ${Math.round(mm.energy_kcal || 0)} kcal
                        </td>
                    </tr>
                </tfoot>
            </table>
        </div>
        ${meal.instructions ? `
        <div class="p-8 bg-white/5 border border-white/5 rounded-3xl text-sm text-slate-300 leading-relaxed italic">
            <p class="font-black text-emerald-400 uppercase text-[10px] mb-2">Příprava:</p>
            ${meal.instructions}
        </div>` : ""}
    </div>`;
}
