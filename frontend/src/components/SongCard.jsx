import React from "react";

function SongCard({song, navigate, setChordsDetail}){
    const formatedDate = new Date(song.created_at).toLocaleDateString("en-MG")
    return (
        <div className="card" ><div className="card-details">
            <p className="text-title">{song.title} <br/> {song.artist}</p>
            <p className="text-body">{formatedDate}</p>
            </div>
            <button className="card-button" onClick={()=>{setChordsDetail(song);navigate(true)}}> details</button>
        </div>
    )
}

export default SongCard