import react from "react"
import { BrowserRouter, Route,Routes,Navigate} from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoutes" 
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"
import NotFound from "./pages/NotFound"

function RegisterAndLogout(){
  localStorage.clear()
  return <Register/>
}
 
function LogOut(){
  localStorage.clear()
  return <Navigate to="/login"/>
}

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route 
      path="/"
      element={
      <ProtectedRoute>
        <Home/>
      </ProtectedRoute>
    }/>
    <Route path="/login" element={<Login/>}/>
    <Route 
      path="/logout"
      element={<LogOut/>}/>
      <Route 
      path="/register"
      element={<RegisterAndLogout/>}/>
      <Route 
      path="*"
      element={<NotFound/>}/>
    </Routes>
    </BrowserRouter>
  )
}

export default App
