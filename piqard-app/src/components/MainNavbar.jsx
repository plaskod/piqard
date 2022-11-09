import React from 'react';
import {Navbar, Nav, Container} from 'react-bootstrap'

import './MainNavbar.css'

function MainNavbar(){
    return(
        <Navbar bg="dark" variant="dark" className='main-navbar'>
        <Container>
          <Navbar.Brand href="/">PIQARD</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/benchmarks">Benchmarks</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    )
}

export default MainNavbar;