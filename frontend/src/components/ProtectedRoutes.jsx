import { ACCESS_TOKEN,REFRESH_TOKEN} from "../constants";
import {jwtDecode} from "jwt-decode"
import {Navigate} from "react-router-dom"
import api from "../api"
import { useState, useEffect } from "react";

function ProtectedRoute({children}){
    const [isAuthorized, setIsAuthorized] = useState(null)

    const auth = async () =>{
        const token = localStorage.getItem(ACCESS_TOKEN)
        if(!token){
            setIsAuthorized(false)
        }else{
        const decoded = jwtDecode(token)
        const expirationDate = decoded.exp
        const now = Date.now() /1000
        if(expirationDate < now){
            await refreshToken()
        } else{
            setIsAuthorized(true)
        }
        }
    }
    useEffect(()=> {
        auth().catch(()=> setIsAuthorized(false))
    },[])

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN)
        try {
            const res = await api.post("/api/token/refresh/",{refresh: refreshToken});
            if(res.status === 200){
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setIsAuthorized(true)
            }else {
                setIsAuthorized(false)
            }
        } catch (error) {
            console.log(error)
            setIsAuthorized(false)
        }
    }

    if (isAuthorized === null){
        return <div>Is Loading ...</div>
    }
    return isAuthorized ? children: <Navigate to="/login"/>
}

export default ProtectedRoute