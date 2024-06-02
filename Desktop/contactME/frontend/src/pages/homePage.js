import { useContext } from "react";
// import UserInfo from "../components/UserInfo";
import AuthContext from "../context/AuthContext";
import MyCarousel from "../components/Carousel";
import React, { useState, useEffect } from 'react';
import { Breadcrumb, Button, ButtonGroup, Row, Col, InputGroup, Form, Image, Dropdown, Card, Table } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faPlus, faCog, faCheck, faSearch, faSlidersH } from '@fortawesome/free-solid-svg-icons';
import users from './Users';
import { Route, Switch, Redirect } from "react-router-dom";
import { Routes } from "../routes";
import { Sidebar, Login } from "../components";
import Modal from 'react-bootstrap/Modal';

const Home = ({ component: Component, ...rest }) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const { registerUser } = useContext(AuthContext);
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [validated, setValidated] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    const first_name = e.target.first_name;
    const last_name = e.target.last_name;
    const email = e.target.email;
    const phone = e.target.phone;
    console.log(first_name,last_name)

    const form = e.currentTarget;
    if (form.checkValidity() === false) {
      e.preventDefault();
      e.stopPropagation();
    }

    setValidated(true);
    // registerUser(first_name, last_name, email,phone);
  };


  return (
    <section>
        <div className="container-fluid">
        <div className="row">
        <div className="col-3">
        <Sidebar />
        </div>
        <div className="col-8">
        <div className="d-lg-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
        <div className="mb-4 mb-lg-0">
        {/* <Breadcrumb className="d-none d-md-inline-block" listProps={{ className: "breadcrumb-dark breadcrumb-transparent" }}>
            <Breadcrumb.Item><FontAwesomeIcon icon={faHome} /></Breadcrumb.Item>
            <Breadcrumb.Item active>Profile</Breadcrumb.Item>
            <Breadcrumb.Item>Contacts</Breadcrumb.Item>
        </Breadcrumb> */}
        <h4>Contact List</h4>
        <p className="mb-0 text-uppercase">A home for all your business or personal contacts</p>
    </div>
    <div className="btn-toolbar mb-2 mb-md-0">
        <Button variant="primary" size="sm" onClick={handleShow}>
            <FontAwesomeIcon icon={faPlus} className="me-2" /> Add New Contact
        </Button>
        <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>New Contact</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                required
                type="text"
                placeholder="Enter First Name"
                onChange={e => setFirstName(e.target.value)}
              />
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
              <Form.Control.Feedback type="invalid">
            Please provide a valid first name.
          </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Last Name"
                required
              />
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
              <Form.Control.Feedback type="invalid">
            Please provide a valid last name.
          </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                required
                type="email"
                placeholder="name@example.com"
                autoFocus
              />
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
              <Form.Control.Feedback type="invalid">
            Please provide a valid email.
          </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Phone</Form.Label>
              <Form.Control
                required
                type="text"
                placeholder="Enter Phone Number"
                autoFocus
              />
            </Form.Group>
            {/* <Form.Group
              className="mb-3"
              controlId="exampleForm.ControlTextarea1"
            >
              <Form.Label>Example textarea</Form.Label>
              <Form.Control as="textarea" rows={3} />
            </Form.Group> */}
          </Form>
        </Modal.Body>
        <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Save Contact
          </Button>
        </Modal.Footer>
      </Modal>
        <ButtonGroup className="ms-3">
            <Button variant="outline-primary" size="sm">Share</Button>
            <Button variant="outline-primary" size="sm">Export</Button>
        </ButtonGroup>
    </div>
    </div>
    <div className="table-settings mb-4">
    <Row className="justify-content-between align-items-center">
        <Col xs={9} lg={4} className="d-flex">
            <InputGroup className="me-2 me-lg-3">
                <InputGroup.Text>
                    <FontAwesomeIcon icon={faSearch} />
                </InputGroup.Text>
                <Form.Control type="text" placeholder="Search" />
            </InputGroup>
            <Form.Select className="w-25">
                <option defaultChecked>All</option>
                <option value="1">Active</option>
                <option value="2">Inactive</option>
                <option value="3">Pending</option>
                <option value="3">Canceled</option>
            </Form.Select>
        </Col>
        <Col xs={3} lg={8} className="text-end">
            <Dropdown as={ButtonGroup} className="me-2">
                <Dropdown.Toggle split as={Button} variant="link" className="text-dark m-0 p-0">
                    <span className="icon icon-sm icon-gray">
                        <FontAwesomeIcon icon={faSlidersH} />
                    </span>
                </Dropdown.Toggle>
                <Dropdown.Menu className="dropdown-menu-right">
                    <Dropdown.Item className="fw-bold text-dark">Show</Dropdown.Item>
                    <Dropdown.Item className="d-flex fw-bold">
                        10 <span className="icon icon-small ms-auto"><FontAwesomeIcon icon={faCheck} /></span>
                    </Dropdown.Item>
                    <Dropdown.Item className="fw-bold">20</Dropdown.Item>
                    <Dropdown.Item className="fw-bold">30</Dropdown.Item>
                </Dropdown.Menu>
            </Dropdown>
            <Dropdown as={ButtonGroup}>
                <Dropdown.Toggle split as={Button} variant="link" className="text-dark m-0 p-0">
                    <span className="icon icon-sm icon-gray">
                        <FontAwesomeIcon icon={faCog} />
                    </span>
                </Dropdown.Toggle>
                <Dropdown.Menu className="dropdown-menu-right">
                    <Dropdown.Item className="fw-bold text-dark">Show</Dropdown.Item>
                    <Dropdown.Item className="d-flex fw-bold">
                        10 <span className="icon icon-small ms-auto"><FontAwesomeIcon icon={faCheck} /></span>
                    </Dropdown.Item>
                    <Dropdown.Item className="fw-bold">20</Dropdown.Item>
                    <Dropdown.Item className="fw-bold">30</Dropdown.Item>
                </Dropdown.Menu>
            </Dropdown>
        </Col>
    </Row>
</div>
<Card border="light" className="table-wrapper table-responsive shadow-sm">
    <Card.Body>
        <Table hover className="user-table align-items-center">
            <thead>
                <tr>
                    <th className="border-bottom">Name</th>
                    <th className="border-bottom">Email</th>
                    <th className="border-bottom">Position</th>
                    <th className="border-bottom">User Created at</th>
                </tr>
            </thead>
            <tbody>
            {users.map(u => (
                <tr key={u.key}>
                    <td>
                        <Card.Link className="d-flex align-items-center">
                            <Image src={u.image} className="user-avatar rounded-circle me-3 contact-list" />
                            <div className="d-block">
                                <span className="fw-bold">{u.name}</span>

                            </div>
                        </Card.Link>
                    </td>
                    <td><span className="fw-normal"><div className="small text-gray">{u.email}</div></span></td>
                    <td><span className="fw-normal"><div className="small text-gray">{u.position}</div></span></td>
                    <td><span className="fw-normal">{u.dateCreated}</span></td>
                </tr>
            ))}
            </tbody>
        </Table>
    </Card.Body>
</Card>
     
        </div>
        </div>
        </div>
    </section>
  );
};

export default Home;