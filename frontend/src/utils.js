/**
 * utils.js — sdílené pomocné funkce
 */

/** Formátuje číslo na N desetinných míst */
export const fmt = (n, dec = 0) =>
    n == null ? "—" : Number(n).toFixed(dec);

/** Formátuje gramy — přes 1000g zobrazí kg */
export const fmtG = (g) =>
    g >= 1000 ? `${(g / 1000).toFixed(2)} kg` : `${Math.round(g)} g`;

/** Součet makra přes pole ingrediencí (pro jednoho uživatele) */
export function sumMacros(ingredients, user = "radim") {
    const key = user === "radim" ? "macros_radim" : "macros_monika";
    return ingredients.reduce((acc, ing) => {
        const m = ing[key] || {};
        return {
            energy_kcal: (acc.energy_kcal || 0) + (m.energy_kcal || 0),
            protein_g:   (acc.protein_g   || 0) + (m.protein_g   || 0),
            carbs_g:     (acc.carbs_g     || 0) + (m.carbs_g     || 0),
            fat_g:       (acc.fat_g       || 0) + (m.fat_g       || 0),
        };
    }, {});
}

/** Procento z cílového příjmu */
export const pct = (val, target) =>
    target > 0 ? Math.min(100, Math.round(val / target * 100)) : 0;

/** Mapování typu jídla na český název */
export const MEAL_LABELS = {
    breakfast: "Snídaně",
    lunch:     "Oběd",
    dinner:    "Večeře",
    snack:     "Svačina",
};

export const DAY_NAMES = ["Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle"];
