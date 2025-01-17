import './App.css'
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from "./pages/login/Login"
import AuthType from './enum/Auth'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login action={AuthType.LOGIN} />} />
        <Route path="/login" element={<Login action={AuthType.LOGIN} />} />
        <Route path="/register" element={<Login action={AuthType.REGISTER} />} />
      </Routes>
    </Router>
  )
}

export default App
