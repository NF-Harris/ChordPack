import React from "react"

function Search({searchTerm, setSearchTerm, searchItem}){

    return <div>
        <div>
            <input className="search"
            type="text"
            value={searchTerm}
            placeholder={searchItem}
            onChange={(e)=> setSearchTerm(e.target.value)}
            />
        </div>
    </div>
}

export default Search