import React from "react";
import "../styles/ChordProConverter.css"
import { useEffect } from "react";

function Convert ({chordProText, setChordProText, content}){
    // Exemple de texte ChordPro (Aznavour - Hier encore)

  // Fonction de parsing ChordPro vers la structure demandée
  const parseChordPro = (text) => {
    const lines = text.split('\n');
    useEffect(()=>{
        setChordProText(content)
    },[])

    return lines.map((line, lineIndex) => {
      // Étape 1 : Si la ligne est complètement vide
      if (line.trim() === "") {
        return <div key={lineIndex} className="blank-line"></div>;
      }

      // Étape 2 : Si la ligne contient des accords en ligne
      const chordRegex = /\[([^\]]+)\]/g;
      
      // Si la ligne n'a pas d'accord, on l'affiche normalement
      if (!line.match(chordRegex)) {
        return (
          <div key={lineIndex} className="lyrics-line">
            {line.startsWith('&nbsp;') ? `\u00A0${line.replace('&nbsp;', '')}` : line}
          </div>
        );
      }

      // Découpage et reconstruction de la ligne avec les accords
      const elements = [];
      let lastIndex = 0;
      let match;

      // On réinitialise la regex pour la boucle
      chordRegex.lastIndex = 0;

      while ((match = chordRegex.exec(line)) !== null) {
        const chordName = match[1];
        const textBefore = line.substring(lastIndex, match.index);

        // Ajouter le texte avant l'accord (s'il y en a)
        if (textBefore) {
          // Gestion du &nbsp; proprement en React
          const cleanText = textBefore.replace(/&nbsp;/g, '\u00A0');
          elements.push(cleanText);
        }

        // Ajouter l'accord au format exact de la photo
        elements.push(
          <span 
            key={`chord-${match.index}`} 
            className="chords" 
            data-chords={chordName} 
            data-display-chords={chordName}
          >
            {/* Le ::before en CSS se chargera d'afficher le texte de l'accord */}
          </span>
        );

        lastIndex = chordRegex.lastIndex;
      }

      // Ajouter le reste du texte après le dernier accord
      if (lastIndex < line.length) {
        const textAfter = line.substring(lastIndex).replace(/&nbsp;/g, '\u00A0');
        elements.push(textAfter);
      }

      return (
        <div key={lineIndex} className="lyrics-line has-outline-chords">
          {elements}
        </div>
      );
    });
  };

  return (
    <div className="converter-container"> 
      <div className="output-container">
        <div className="song-sheet">
          {parseChordPro(chordProText)}
        </div>
      </div>
    </div>
  );
}

export default Convert