import React from 'react';
import axios from 'axios';
import Table from 'react-bootstrap/Table';

const ContactAPI = () => {
  const state = {
    results: []
  }

//   componentDidMount() {
//     axios.get(`http://127.0.0.1:8000/api/`)
//       .then(res => {
//         const results = res.data;
//         this.setState({results:results.results});
//         console.log({results:results.results})
//       })
//   }

    return (
        <>
      <div className='container-fluid'>
       
                <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Username</th>
                  </tr>
                </thead>
                <tbody>
                {state.results
                    .map(result =>
                  <tr>
                    <td key={result.id}>{result.id}</td>
                    <td>{result.first_name}</td>
                    <td>{result.last_name}</td>
                    <td>{result.email}</td>
                  </tr>
                )}
                </tbody>
              </Table>                 
      </div>
      </>
    )
  }

export default ContactAPI;