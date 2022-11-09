import { Container, Row, Col, Button } from "react-bootstrap";

import './HomeView.css'

function HomeView(){
    return(
        <Container fluid className="main-hero">
            <Row>
                <Col md={7} className="hero-col">
                    <div class='image'>

                    </div>
                </Col>
                <Col md={5} className="center">
                    <div>
                        <h1>Prompting is the future!</h1>
                        <Container className="center hero-col">
                            <Button>Get started now</Button>
                        </Container>
                    </div>
                </Col>
            </Row>
        </Container>
    )
}

export default HomeView;