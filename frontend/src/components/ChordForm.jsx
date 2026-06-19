import React from "react";

function ChordForm({createUserChords,setUserChordTitle,userChordTitle,setUserChordArtist,userChordArtist,setUserChordContent,userChordContent}){
    return <div className="column-layout">
            <h2>Ecrivez vos partitions ici</h2>
            <form onSubmit={createUserChords}>
                <label htmlFor="title">Titre</label>
                <br/>
                <input
                type="text"
                name="userchordtitle"
                id="userchordtitle"
                required
                onChange={(e)=> setUserChordTitle(e.target.value)}
                value={userChordTitle}
                />
                <br/>
                <label htmlFor="artist">Artiste</label>
                <br/>
                <input
                type="text"
                name="artist"
                id="artist"
                required
                onChange={(e)=> setUserChordArtist(e.target.value)}
                value={userChordArtist}
                />
                <br/>
                <label htmlFor="content">Partitions</label>
                <br/>
                <textarea
                placeholder="Exemple:
                G                  C
Une souris verte qui courait dans l'herbe
         D7                  G
Je la chope par la queue, je la montre à ces messieurs
           G                    C
Ces messieurs me disent : trempez-la dans l'huile
           D7                   G
Trempez-la dans l'eau, ça fera un escargot tout chaud"
                type="text"
                name="userchordcontent"
                id="userchordcontent"
                required
                onChange={(e)=> setUserChordContent(e.target.value)}
                value={userChordContent}
                />
                <br/>
                <input type="submit" value="submit"/>
            </form>
            </div>
}

export default ChordForm