import React from "react";
import Convert from "../components/Convert"

function ChordCard ({song, navigate, loading,
    chordProText, setChordProText, isPrivate, deleteChord, rectify}){
    const formatedDate = new Date(song.created_at).toLocaleDateString("en-MG")
    return <div className="chord">
                <div className="chord-details">
                    <p className="text-title">{song.title}</p>
                    <p className="text-title">{song.artist}</p>
                    <Convert chordProText={chordProText} setChordProText={setChordProText} content={song.content}/>
                    <p className="chord-date">{formatedDate}</p>
                    <div className="layout">
                    <button onClick={()=>{navigate(false)}} className="btn-blue"> retour </button>
                    {song.verified === true?<div></div>:loading?<button >loading...</button>:
                    <button onClick={()=> rectify(song.id)} className="btn-blue">rectifier</button>}
                    {isPrivate? <button className="btn-red" onClick={()=>{deleteChord(song.id);navigate(false)}}>supprimer </button>: null}
                    </div>
                    <p>Rafraichir la page apres une rectification
                        <br/>***Il s'agit d'une rectification de mise en page par IA*** </p>
                </div>
            </div>}
export default ChordCard