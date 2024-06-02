import {React, useState} from 'react'
import './App.css'
import './custom.css'
import { BrowserRouter as Router, Routes, Route,Switch, Link } from 'react-router-dom'
import { SignUp, Login, ContactForm } from './components'
import Navbar from './components/Navbar'
// import Footer from "./components/Footer";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/homePage";
import { ProtectedPage, isLoading } from "./utils";

function App() {

  return (
    <Router>
      <div className="flex flex-col min-h-screen overflow-hidden">
        <AuthProvider>
          <Navbar />
          <Switch>
            <Route component={ProtectedPage} path="/protected" exact />
            <Route component={Login} path="/sign-in" />
            <Route component={SignUp} path="/sign-up" />
            <Route component={Home} path="/" />
            <Route component={ContactForm} path="/contact" />
            {/* <Route exact path="/" component={ContactAPI}/>  */}
            {/* <Route path="/sign-in" element={<Login />} /> */}
            {/* <Route path="/sign-up" element={<SignUp />} /> */}
    
            <Route path="/contact"> <ContactForm /> </Route>
            {/* <Route path="/" element={<ContactAPI />} />  */}
          </Switch>
        </AuthProvider>
      </div>
    </Router>
  );
}
export default App