import { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";

function SignUp() {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const { registerUser } = useContext(AuthContext);

  const handleSubmit = async e => {
    e.preventDefault();
    registerUser(first_name, last_name, email,phone);
  };

  return (
    <section>
        <div className="container">
      <form onSubmit={handleSubmit}>
        <h1>Register</h1>
        <hr />
        <div>
          <label htmlFor="first_name">First Name</label>
          <input
            type="text"
            id="first_name"
            className="form-control"
            onChange={e => setFirstName(e.target.value)}
            placeholder="First Name"
            required
          />
        </div>
        <div>
          <label htmlFor="last_name">Last Name</label>
          <input
            type="text"
            id="last_name"
            className="form-control"
            onChange={e => setLastName(e.target.value)}
            placeholder="Last Name"
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            className="form-control"
            id="email"
            onChange={e => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
          {/* <p>{password2 !== password ? "Passwords do not match" : ""}</p> */}
        </div>
        <div>
          <label htmlFor="phone">Phone</label>
          <input
            type="text"
            id="phone"
            className="form-control"
            onChange={e => setPhone(e.target.value)}
            placeholder="Phone"
            required
          />
        </div>
        <div className="mt-4">
        <button
        className="form-control btn btn-primary"
        >Register</button>
        </div>
       
      </form>
      </div>
    </section>
  );
}

export default SignUp;