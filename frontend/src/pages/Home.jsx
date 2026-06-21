import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api"
import apiSimple from "../apiSimple"
import Note from "../components/Note"
import Search from "../components/Search"
import SongCard from "../components/SongCard"
import ChordCard from "../components/ChordCard"
import ChordForm from "../components/ChordForm"
import "../styles/switch.css"
import ConvertToChord from "../ConvertToChord"


function Home(){
    const [notes, setNotes] = useState([])
    const [chords, setChords] = useState([])
    const [content, setContent] = useState("")
    const [title, setTitle] = useState("")
    const [searchTerm, setSearchTerm] = useState("")
    const [method, setMethod] = useState("")
    const [chordContent, setChordContent] = useState("")
    const [chordTitle, setChordTitle] = useState("")
    const [chordArtist, setChordArtist] = useState("")
    const [seeDetail, setSeeDetail] = useState(false)
    const [change,setChange] = useState(false)
    const [chordDetail, setChordDetail] = useState(null)
    const [isPrivate, setIsPrivate] = useState(false)
    const [chordProText, setChordProText] = useState("");
    const [userChordTitle, setUserChordTitle] = useState("")
    const [userChordArtist, setUserChordArtist] = useState("")
    const [userChordContent, setUserChordContent] = useState("")
    const [userChords, setUserChords] = useState([])
    const [nextPage,setNextPage] = useState("")
    const [prevPage,setPrevPage] = useState("")
    const [goNext, setGoNext] = useState(false)
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    

     

    const navigate = useNavigate()
    

    useEffect(()=>{
            getNotes()
            getChords()
            getUserChords()
        },[])
        
    useEffect(() => {
        const handler = setTimeout(() => {
            isPrivate? getUserChords() :getChords();
        }, 500); // 500 millisecondes (ajuste à ta guise)

        return () => {
            clearTimeout(handler);
        };
    }, [chordArtist, chordTitle, chordContent]);


    const getNotes = async () => {
        try{
            const res = await api.get("/api/notes/")
            console.log(res.data)
            setNotes(res.data.results || [])

        }catch(error){
            if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }}}

    const getChords = async () => {
        try{
            const filter = {}
            if(chordArtist) {filter.artist__icontains = chordArtist}
            if(chordContent) {filter.content__icontains = chordContent}
            if(chordTitle) {filter.title__icontains = chordTitle }

            const res = await api.get("api/chords/public/", {params: filter})
            console.log(res.data)
            setChords(res.data.results || [])
            setNextPage(res.data.next)
            setPrevPage(res.data.previous)

        }catch(error){
            if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
        }
    }
    const rectify = async (id)=>{
        setLoading(true);
        setError(null);

        try{
            const res = await api.post(`api/chords/rectify/${id}/`)
            setChordDetail(res.data)

        }catch (err) {
      if (err.response && err.response.status === 429) {
        // On récupère les données structurées par notre backend Django
        const { message, wait_seconds } = err.response.data;
        
        let friendlyMessage = message;
        if (wait_seconds) {
          friendlyMessage += ` Veuillez réessayer dans ${Math.ceil(wait_seconds / 60)} minute(s).`;
        }
        
        setError(friendlyMessage);
      } else {
        setError("Une erreur inattendue est survenue.");
      }
    } finally {
      setLoading(false);
    }}
                
    const deleteChord = async (id)=>{
        try{
            const res = await api.delete(`api/chords/user/update/${id}/`)
            if(res.status ===204 ){
                getUserChords()
            }
            
        }
        catch(error){
            if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
        }
    }
    const createNotes = async (e) => {
        e.preventDefault()
        try{
            const res = await api.post("/api/notes/", { content, title})
        if(res.status ===201 ){
                alert("Note Created")
                getNotes()
            }
            else {alert("Failed to create note")}}
            catch(error){
                if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
            }
    }

    const createUserChords = async (e) => {
        e.preventDefault()
        try{
            const contentChord = ConvertToChord(userChordContent)
            const res = await api.post("/api/chords/user/", { title:userChordTitle, artist:userChordArtist, content:contentChord})
        if(res.status ===201 ){
                getUserChords()
            }
            else {alert("Failed to create note")}}
            catch(error){
                if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
            }
    }

    const getUserChords = async () => {
        try{
            const filter = {}
            if(chordArtist) {filter.artist__icontains = chordArtist}
            if(chordContent) {filter.content__icontains = chordContent}
            if(chordTitle) {filter.title__icontains = chordTitle }

            const res = await api.get("api/chords/user/", {params: filter})
            console.log(res.data)
            setUserChords(res.data.results || [])

        }catch(error){
            if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
        }
    }

    const getNextChords = async (direction) => {
        try{
            const url = direction === "next"? nextPage: prevPage
            if (!url) {return}

            const res = await apiSimple.get(url)
            console.log(res.data)
            setChords(res.data.results || [])
            setNextPage(res.data.next)
            setPrevPage(res.data.previous)

        }catch(error){
            if (error.response && error.response.data) {
                console.log("Erreurs du serveur :", error.response.data);
            alert(JSON.stringify(error.response.data));
            }else {
                console.log("Erreur générale :", error.message);
                alert(error.message);
                }
        }
    }
        
    return (
    <div className="wrapper">
        <header>
            <div className="search-container">
                <Search searchItem="Artiste" searchTerm={chordArtist} setSearchTerm={setChordArtist}/>
                <Search searchItem="Titre" searchTerm={chordTitle} setSearchTerm={setChordTitle}/>
                <Search searchItem="Paroles" searchTerm={chordContent} setSearchTerm={setChordContent}/>
                <div>
                    <label className="switch">
                        <input type="checkbox"
                        onChange={()=>{setIsPrivate(!isPrivate); setSeeDetail(false)}}/>
                        <span className="slider"></span>
                    </label>
                </div>
                <div className="Btn-container">
                    <button className="Btn" onClick={()=>navigate("/logout")}>
                    
                    <div className="sign"><svg viewBox="0 0 512 512"><path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path></svg></div>
                    
                    <div className="text">Logout</div>
                    </button>
                </div>
            </div>
        </header>
        <div>Chansons:
        </div>
            {isPrivate ? 
            <section>{ userChords && userChords.length > 0?
                <div className="column-layout">
                <section>
                {seeDetail ? <ChordCard song={chordDetail} navigate={setSeeDetail} 
                chordProText={chordProText} setChordProText={setChordProText}
                deleteChord={deleteChord} isPrivate={isPrivate} ChordId={chordDetail.id}/> :
                <ul className="layout">{userChords.map((chord)=> (<SongCard song={chord} key={chord.id} navigate={setSeeDetail} setChordsDetail={setChordDetail}/>))}
                </ul>}
                </section>
                </div>
                :<div class="no-chord">
                    <span>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="m256 8c-136.957 0-248 111.083-248 248 0 136.997 111.043 248 248 248s248-111.003 248-248c0-136.917-111.043-248-248-248zm0 110c23.196 0 42 18.804 42 42s-18.804 42-42 42-42-18.804-42-42 18.804-42 42-42zm56 254c0 6.627-5.373 12-12 12h-88c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h12v-64h-12c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h64c6.627 0 12 5.373 12 12v100h12c6.627 0 12 5.373 12 12z"
                        >
                        </path>
                        </svg>
                        <p>Aucune partitions pour l'instant</p>
                    </span>
                </div>}
                <div className="layout">
                    <div>
                    <ChordForm createUserChords={createUserChords} setUserChordTitle={setUserChordTitle} userChordTitle= {userChordTitle} 
                    setUserChordArtist={setUserChordArtist} userChordArtist={userChordArtist} setUserChordContent={setUserChordContent} userChordContent={userChordContent}/>
                </div>
                </div>
            </section> :
            <div className="column-layout">
                <section>{seeDetail ? <ChordCard song={chordDetail} loading={loading} rectify={rectify} navigate={setSeeDetail} chordProText={chordProText} setChordProText={setChordProText}/> :
                    <ul className="layout">{chords.map((chord)=> (<SongCard song={chord} key={chord.id} navigate={setSeeDetail} setChordsDetail={setChordDetail}/>))}
                    </ul>}
                </section>
                <div className="button-layout">
                    <button onClick={()=>{getNextChords("prev")}} disabled={!prevPage || seeDetail}>Previous</button>
                    <button onClick={()=>{getNextChords("next")}} disabled={!nextPage || seeDetail}>Next</button>
                </div>
            </div>}
    </div>
    );
}
export default Home