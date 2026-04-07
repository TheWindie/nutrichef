/**
 * components.js — HTML generátory pro opakující se UI bloky
 */
import { fmt, fmtG, MEAL_LABELS } from "./utils.js";

/** Karta s makry pro jednoho uživatele */
export function macroCard({ name, kcal, protein, carbs, fat, target, color }) {
    const pct = target > 0 ? Math.min(100, Math.round(kcal / target * 100)) : 0;
    const over = kcal > target * 1.1;
    const kcalColor = over ? "text-red-400" : "text-white";
    return `
    <div class="bg-${color}-500/10 p-6 rounded-3xl border border-${color}-500/20 w-48 shadow-inner">
        <p class="text-[9px] font-black uppercase text-${color}-400 mb-1 tracking-widest">${name}</p>
        <p class="text-3xl font-black ${kcalColor}">${Math.round(kcal)} kcal</p>
        <p class="text-[9px] text-${color}-400/70 font-bold mt-1">
            B:${fmt(protein,1)}g &nbsp;S:${fmt(carbs,1)}g &nbsp;T:${fmt(fat,1)}g
        </p>
        <div class="mt-3 h-1.5 rounded-full bg-white/10 overflow-hidden">
            <div class="h-full bg-${color}-400 rounded-full transition-all" style="width:${pct}%"></div>
        </div>
        <p class="text-[9px] text-${color}-400/50 mt-1">${pct}% cíle ${over ? "⚠️" : ""}</p>
    </div>`;
}

/**
 * Řádek tabulky s ingrediencí — editovatelné gramy + live přepočet.
 * data-food-* atributy nesou nutriční hodnoty /100g pro JS přepočet.
 */
export function ingredientRow(ing) {
    const mr = ing.macros_radim  || {};
    const mm = ing.macros_monika || {};
    const f  = ing.food_data     || {};   // nutriční hodnoty /100g (z API enrichmentu)
    return `
    <tr class="border-b border-white/5 text-[11px] hover:bg-white/5 transition-colors group"
        data-kcal100="${f.energy_kcal||0}" data-prot100="${f.protein_g||0}"
        data-carb100="${f.carbs_g||0}" data-fat100="${f.fat_g||0}">
        <td class="py-3 font-bold text-slate-300 group-hover:text-white sticky-col pr-3">${ing.food_name}</td>
        <td class="py-3 text-center">
            <input type="number" min="0" max="9999" step="1"
                value="${ing.amount_radim_g}"
                class="amount-input w-16 bg-emerald-500/10 border border-emerald-500/30
                       text-emerald-400 font-black text-center rounded-xl px-2 py-1
                       focus:outline-none focus:border-emerald-400 transition"
                data-user="r">
        </td>
        <td class="py-3 text-center text-emerald-100 val-r-kcal">${fmt(mr.energy_kcal)}</td>
        <td class="py-3 text-center text-emerald-100 val-r-prot">${fmt(mr.protein_g,1)}</td>
        <td class="py-3 text-center text-emerald-100 val-r-carb">${fmt(mr.carbs_g,1)}</td>
        <td class="py-3 text-center text-emerald-100 val-r-fat">${fmt(mr.fat_g,1)}</td>
        <td class="py-3 text-center border-l border-white/10">
            <input type="number" min="0" max="9999" step="1"
                value="${ing.amount_monika_g}"
                class="amount-input w-16 bg-rose-500/10 border border-rose-500/30
                       text-rose-400 font-black text-center rounded-xl px-2 py-1
                       focus:outline-none focus:border-rose-400 transition"
                data-user="m">
        </td>
        <td class="py-3 text-center text-rose-100 val-m-kcal">${fmt(mm.energy_kcal)}</td>
        <td class="py-3 text-center text-rose-100 val-m-prot">${fmt(mm.protein_g,1)}</td>
        <td class="py-3 text-center text-rose-100 val-m-carb">${fmt(mm.carbs_g,1)}</td>
        <td class="py-3 text-center text-rose-100 val-m-fat">${fmt(mm.fat_g,1)}</td>
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

/** Blok jednoho jídla s live přepočtem */
export function mealBlock(meal) {
    const rows = meal.ingredients.map(ingredientRow).join("");
    const mr = meal.macros_radim  || {};
    const mm = meal.macros_monika || {};
    const mealId = `meal-${meal.id}`;
    return `
    <div class="space-y-6" id="${mealId}">
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
                <tbody class="meal-tbody">${rows}</tbody>
                <tfoot class="bg-white/10 font-black text-[12px] text-white">
                    <tr>
                        <td class="p-5 px-6 uppercase tracking-widest text-[10px] sticky-col">SOUČET</td>
                        <td colspan="5" class="p-5 text-center text-emerald-400 underline decoration-2 decoration-emerald-800 meal-total-r">
                            ${Math.round(mr.energy_kcal || 0)} kcal
                        </td>
                        <td colspan="5" class="p-5 text-center text-rose-400 border-l border-white/10 underline decoration-2 decoration-rose-800 meal-total-m">
                            ${Math.round(mm.energy_kcal || 0)} kcal
                        </td>
                    </tr>
                </tfoot>
            </table>
        </div>
        ${meal.instructions ? `
        <div class="p-6 bg-white/5 border border-white/5 rounded-3xl text-sm text-slate-300 leading-relaxed italic">
            <p class="font-black text-emerald-400 uppercase text-[10px] mb-2">Příprava:</p>
            ${meal.instructions}
        </div>` : ""}
    </div>`;
}

/**
 * Připne live přepočet na všechny amount-input v daném elementu.
 * Volej po každém renderMenu().
 */
export function bindLiveCalc(root) {
    root.querySelectorAll(".amount-input").forEach(input => {
        input.addEventListener("input", () => recalcRow(input));
    });
}

function recalcRow(input) {
    const row   = input.closest("tr");
    const grams = parseFloat(input.value) || 0;
    const f     = parseFloat(input.value) >= 0 ? grams / 100 : 0;
    const kcal100 = parseFloat(row.dataset.kcal100) || 0;
    const prot100 = parseFloat(row.dataset.prot100) || 0;
    const carb100 = parseFloat(row.dataset.carb100) || 0;
    const fat100  = parseFloat(row.dataset.fat100)  || 0;
    const user    = input.dataset.user;  // "r" nebo "m"

    const kcal = (kcal100 * f).toFixed(0);
    const prot = (prot100 * f).toFixed(1);
    const carb = (carb100 * f).toFixed(1);
    const fat  = (fat100  * f).toFixed(1);

    row.querySelector(`.val-${user}-kcal`).textContent = kcal;
    row.querySelector(`.val-${user}-prot`).textContent = prot;
    row.querySelector(`.val-${user}-carb`).textContent = carb;
    row.querySelector(`.val-${user}-fat`).textContent  = fat;

    // Přepočítej součet jídla
    const tbody = row.closest("tbody");
    recalcMealTotal(tbody, user);
}

function recalcMealTotal(tbody, user) {
    let total = 0;
    tbody.querySelectorAll(`.val-${user}-kcal`).forEach(cell => {
        total += parseFloat(cell.textContent) || 0;
    });
    const tfoot = tbody.closest("table").querySelector("tfoot");
    const cls = user === "r" ? ".meal-total-r" : ".meal-total-m";
    const cell = tfoot.querySelector(cls);
    if (cell) cell.textContent = `${Math.round(total)} kcal`;
}
