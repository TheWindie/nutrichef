/**
 * api.js — všechna komunikace s FastAPI backendem
 * Základní URL se bere z window.location — funguje lokálně i v Dockeru.
 */
const BASE = "/api";

async function apiFetch(path, opts = {}) {
    const res = await fetch(BASE + path, {
        headers: { "Content-Type": "application/json" },
        ...opts,
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || "API chyba");
    }
    return res.json();
}

export const api = {
    // Potraviny
    getFoods:      (search = "", cat = "") =>
        apiFetch(`/foods/?search=${encodeURIComponent(search)}&category=${cat}`),
    getFood:       (id)  => apiFetch(`/foods/${id}`),
    createFood:    (body)=> apiFetch("/foods/", { method: "POST", body: JSON.stringify(body) }),
    getCategories: ()    => apiFetch("/foods/categories"),

    // Plány
    getPlans:      ()    => apiFetch("/plans/"),
    getPlan:       (id)  => apiFetch(`/plans/${id}`),
    getShopping:   (id)  => apiFetch(`/plans/${id}/shopping`),
    getMacros:     (id)  => apiFetch(`/plans/${id}/macros`),

    // Uživatelé
    getUsers:      ()    => apiFetch("/users/"),
};
