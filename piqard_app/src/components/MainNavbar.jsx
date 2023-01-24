import React from 'react';
import {Navbar, Nav, Container} from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons'
import { faTwitter } from '@fortawesome/free-brands-svg-icons'

import './MainNavbar.css'


function MainNavbar(){
    return(
        
        <Navbar variant="dark" className='main-navbar' collapseOnSelect expand="sm">
            <Container>
              <Navbar.Brand href="/">PIQARD</Navbar.Brand>
              <Navbar.Toggle />

              <Navbar.Collapse>
                  <Nav className="me-auto">
                    <Nav.Link href="/opensystem">OpenSystem</Nav.Link>
                    {/* <Nav.Link href="/playground">Playground</Nav.Link> */}
                    {/* <Nav.Link href="/benchmarks">Benchmarks</Nav.Link> */}
                  </Nav>

                  <Nav className="justify-content-end" activeKey="/home">
                    <a href='https://github.com/plaskod/piqard' className='a-link'>
                      <div className='social-icon'>
                        <FontAwesomeIcon icon={faGithub} />
                      </div>
                    </a>
                    {/* <div className='social-icon'><FontAwesomeIcon icon={faTwitter} /></div> */}
                  </Nav>
              </Navbar.Collapse>
            </Container> 
        </Navbar>
    )
}

export default MainNavbar;