import { useContext } from "react";
import AuthContext from "../context/AuthContext";

const Login = () => {

    const { loginUser } = useContext(AuthContext);

    const handleSubmit = e => {
        e.preventDefault();

        const username = e.target.username.value;
        const password = e.target.password.value;
        username.length > 0 && loginUser(username, password);
    };

    return (
        <>
        
      <div className="container">
      <form onSubmit={handleSubmit}>
        <h1>Sign In</h1>
        <hr />
        <div className="mb-3">
        <label htmlFor="username">Username</label>
          <input
            type="text"
            id = "username"
            className="form-control"
            placeholder="Enter Username"
          />
        </div>
        <div className="mb-3">
        <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            className="form-control"
            placeholder="Enter Password"
          />
        </div>
        <div className="mb-3">
          <div className="custom-control custom-checkbox">
            <input
              type="checkbox"
              className="custom-control-input"
              id="customCheck1"
            />
            <label className="custom-control-label" htmlFor="customCheck1">
              Remember me
            </label>
          </div>
        </div>
        <div className="d-grid">
          <button type="submit" className="btn btn-primary form-control">
            Login
          </button>
        </div>
        {/* <p className="forgot-password text-right">
          Forgot <a href="#">password?</a>
        </p> */}
      </form>
      </div>
    
  </>
    )
}

export default Login;