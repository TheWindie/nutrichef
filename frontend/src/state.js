/**
 * state.js — globální stav aplikace (jednoduchý reactive store)
 */
export const state = {
    plan: null,
    shopping: null,
    foods: [],
    activeTab: "dash",
    activePlanId: 1,
    users: { radim: { name:"Radim", target:2100, color:"emerald" },
             monika: { name:"Monika", target:1450, color:"rose" } },
};

const listeners = [];
export function subscribe(fn) { listeners.push(fn); }
export function notify()      { listeners.forEach(fn => fn(state)); }

export function setState(patch) {
    Object.assign(state, patch);
    notify();
}
