logic

visible input -> hidden field -> visible input -> hidden field

visible input = made on the spot using js
hidden field = the field in django form

-- Template --
FYE
(pure js)

Fee
1. visible
2. hidden

Termin
1. visible
2. hidden

hidden = variable js yg refer ke field2 nya form
hidden krna kita nge-hide field nya pas di UI

const form = document.getElementById("proposalForm");

const fyeWrapper = document.getElementById("fye-fields");
const addFye = document.getElementById("add-fye");
const hiddenFye = document.getElementById("fye-data");
const errorFye = document.getElementById("fye-error");

fye-input