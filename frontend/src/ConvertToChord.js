

const ConvertToChord = (content) => {
    // 1. On sépare le texte ligne par ligne (remplace \xa0 par un espace standard)
    let lignes = content.replace(/\u00A0/g, " ").split('\n');

    // Nettoyage des lignes vides au début ou à la fin (équivalent du list comprehension)
    lignes = lignes.filter(l => l.trim() !== "" || l === "");

    const chansonChordpro = [];
    const ignoreList = ["Chorus", "Verse", "Intro", "Tondrompeon", "Tonony", "Fiverenana", "Key", "Tonalite","Fampidirana"];

    // 2. On parcourt les lignes
    let i = 0;
    while (i < lignes.length) {
      let ligneActuelle = lignes[i];

      // Vérification de la liste d'exclusion
      let ignore = false;
      for (let ing of ignoreList) {
        if (ligneActuelle.includes(ing)) {
          ignore = true;
          break;
        }
      }

      // S'il s'agit d'une ligne vide ou d'un titre de section
      if (ligneActuelle.trim() === "" || ignore) {
        chansonChordpro.push(ligneActuelle.trim());
        i += 1;
        continue;
      }

      // On vérifie si la ligne suivante existe
      if (i + 1 < lignes.length) {
        let ligneSuivante = lignes[i + 1];

        // Détection : Si la ligne actuelle contient des accords (Pattern Regex réajusté pour JS)
        const chordRegex = /[A-G][#b]?[m0-9]?[^\s]*/g;
        const matchesExist = ligneActuelle.match(chordRegex);

        if (matchesExist && matchesExist.length > 0) {
          
          // --- ALGORITHME DE FUSION EN CHORDPRO ---
          let accordsTrouves = [];
          
          // Équivalent de re.finditer en JS pour choper l'index et l'accord
          const globalWordRegex = /\S+/g;
          let match;
          while ((match = globalWordRegex.exec(ligneActuelle)) !== null) {
            accordsTrouves.push({
              index: match.index,
              accord: match[0]
            });
          }

          // On trie les accords du plus grand index au plus petit (très important !)
          accordsTrouves.sort((a, b) => b.index - a.index);

          // On transforme la ligne de paroles en tableau de caractères pour insérer facilement
          let parolesListe = ligneSuivante.split("");

          for (let item of accordsTrouves) {
            // Si l'accord est positionné plus loin que la longueur du texte, on comble avec des espaces
            if (item.index > parolesListe.length) {
              const diff = item.index - parolesListe.length;
              parolesListe = parolesListe.concat(new Array(diff).fill(" "));
            }

            // On insère l'accord au format ChordPro [Accord] à l'index précis
            parolesListe.splice(item.index, 0, `[${item.accord}]`);
          }

          // On rassemble la ligne fusionnée
          let ligneFusionnee = parolesListe.join("");
          chansonChordpro.push(ligneFusionnee.trim());

          // On avance de 2 lignes puisqu'on a traité accords + paroles
          i += 2;
        } else {
          // C'est une ligne de texte normale sans accord au-dessus
          chansonChordpro.push(ligneActuelle.trim());
          i += 1;
        }
      } else {
        chansonChordpro.push(ligneActuelle.trim());
        i += 1;
      }
    }

    // 3. Résultat final prêt
    const texteFinalChordpro = chansonChordpro.join("\n");
    return texteFinalChordpro
  }

export default ConvertToChord