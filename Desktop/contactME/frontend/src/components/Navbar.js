import { useContext } from "react";
import { BrowserRouter as Router, Link } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
import AuthContext from "../context/AuthContext";
import Container from 'react-bootstrap/Container';

// import Navbar from 'react-bootstrap/Navbar';


const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);
  return (
   
      
        <Nav className="navbar navbar-dark bg-dark justify-content-end">

      
          {user ? (
            <>
              <Nav.Item>
              <Nav.Link href="/" to="/">Home</Nav.Link>
              </Nav.Item>
              <Nav.Item>
              <Nav.Link href="/protected" to="/protected">My List</Nav.Link>
              </Nav.Item>
              <Nav.Item>
              <Nav.Link to="/contact">Contact</Nav.Link>
              </Nav.Item>
              <button className="btn btn-dark" onClick={logoutUser}>Logout</button>
              
            </>
          ) : (
            <>
                 <Nav.Item>
              <Nav.Link href="/" to="/">Home</Nav.Link>
              </Nav.Item>
                <Nav.Item>
                  <Nav.Link href="/sign-in" to="/sign-in">Login </Nav.Link>
                </Nav.Item>
                <Nav.Item>
                <Nav.Link href="/sign-up" to="/sign-up">Register</Nav.Link> 
                  </Nav.Item> 
                  <Nav.Item>
                <Nav.Link to="/contact">Contact Us</Nav.Link> 
                  </Nav.Item>     
            </>
          )}
      
        </Nav>
    
  
  );
};

export default Navbar;