import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

const apiSimple = axios.create({
    headers : {"Content-Type": "application/json"},
})
apiSimple.interceptors.request.use(
    (config) =>{
        const token = localStorage.getItem(ACCESS_TOKEN)
        if(token){
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error)=>{
        return Promise.reject(error)
    }
)

export default apiSimple;