import { useEffect, useState } from "react";
import Table from 'react-bootstrap/Table';
import useAxios from "../utils/useAxios";
import Spinner from "../components/Spinner";

function ProtectedPage() {
  const [res, setRes] = useState("");
  const api = useAxios();
  const [isLoading, setLoading] = useState(true)

  
 
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await api.get("http://localhost:8000/api/");
        setRes({response:response.data.results});
        console.log("Finished api call",response.data.results)
        setLoading(false)

      } catch {
        alert("Something went wrong")
        setLoading(false)
        setRes("Something went wrong");
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="container">
      <h1>MY Contact List</h1>
       
      { isLoading ? <Spinner /> : 
      <Table striped bordered hover variant="dark">
        
                <thead>
                  <tr>
                    <th></th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Username</th>
                  </tr>
                </thead>
                <tbody>
                {/* {
                res.map(result => */}
                  <tr>
                    {/* <td key={result.id}>{result.id}</td>
                    <td>{result.first_name}</td>
                    <td>{result.last_name}</td>
                    <td>{result.email}</td> */}
                  </tr>
                {/* )}  */}
                </tbody>
              </Table> 
}
    </div>
  );
}

export default ProtectedPage;