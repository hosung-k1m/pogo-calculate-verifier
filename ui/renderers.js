import {h} from "./kit/components.js";

function renderIVs({pokemon, spreads}, {verdict}) {
  if (!verdict.valid) return h("p", {text: "The submitted IVs did not pass verification."});
  const root = h("section", {class: "iv-result"}, h("h3", {text: pokemon.replaceAll("_", " ")}));
  if (spreads.length === 0) {
    root.append(h("p", {text: "No IV spread fits these observations. Check the form, encounter, CP, and appraisal."}));
    return root;
  }

  root.append(h("p", {text: spreads.length === 1
    ? "One IV spread fits."
    : `${spreads.length.toLocaleString()} IV spreads fit. Max HP or appraisal can narrow the results.`}));
  const headings = ["Attack IV", "Defense IV", "HP IV", "Pokémon levels"];
  const header = h("thead", {}, h("tr", {}, headings.map(text => h("th", {scope: "col", text}))));
  const body = h("tbody");
  const more = h("button", {type: "button", text: "Show more"});
  root.append(h("table", {}, header, body), more);

  let shown = 0;
  function showMore() {
    for (const {attack, defense, hp, levels} of spreads.slice(shown, shown + 30)) {
      const cells = [attack, defense, hp, levels.join(", ")].map(value => h("td", {text: String(value)}));
      body.append(h("tr", {}, cells));
    }
    shown += 30;
    if (shown >= spreads.length) more.remove();
  }
  more.addEventListener("click", showMore);
  showMore();
  return root;
}

export default {IVOutput: renderIVs};
