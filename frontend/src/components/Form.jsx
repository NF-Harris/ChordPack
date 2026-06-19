import { useState } from "react";
import { useNavigate,Link } from "react-router-dom";
import { ACCESS_TOKEN,REFRESH_TOKEN } from "../constants";
import api from "../api";
import "../styles/Form.css"

function Form({route,method}){
    const [password, setPassword] = useState("")
    const [username,setUsername] = useState("")
    const [errorMessage, setErrorMessage] = useState("")
    const [loading,setLoading] = useState(false)
    const navigate = useNavigate();

    const name = method === "Login"? "Login":"Register"
    const handleSubmit = async (e) =>{
        setLoading(true)
        e.preventDefault()
        try{
            const res = await api.post(route,{username, password})
            if(method ==="Login"){
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh)   
                navigate("/")
            }else {
                navigate("/login")
            }

        }catch (error) {
    if (error.response.data.username && error.response.data.username[0].includes("already exists")) {
        setErrorMessage("Désolé, ce nom d'utilisateur est déjà pris !");
    } else {
        setErrorMessage("Nom d'utilisateur ou mot de passe incorrect.");
    }
        }finally{
            setLoading(false)
        }
    }

    return <form onSubmit={handleSubmit} className="form-container">
        <h1>{name}</h1>
        <input
            className="form-input"
            type="text"
            placeholder="User Name"
            value={username}
            onChange={(e) => {setUsername(e.target.value)}}
        />
        <input
            className="form-input"
            type="password"
            placeholder="PassWord"
            value={password}
            onChange={(e) => {setPassword(e.target.value)}}
        />
        <button className="form-button" type="submit">{name}</button>
        <div>
            {errorMessage && (
    <div className="error-banner">
      ⚠️ {errorMessage}
    </div>
  )}
        </div>
        <div class="form-section">
{method === "Login" ? (
  <p>Don't have an account? <Link to="/register">Register</Link></p>
) : (
  <p>Already have an account? <Link to="/login">Login</Link></p>
)}
</div>

    </form>
}

export default Form