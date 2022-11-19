import { Container, Row, Col } from "react-bootstrap";
import Button from "../components/Button";

import './HomeView.css'

function HomeView(){
    return(
        <Container fluid className="main-hero">
            <Row>
                <Col md={7} className="hero-col">
                    <div className='image'>

                    </div>
                </Col>
                <Col md={5} className="center">
                    <div>
                        <h1>Prompting is the future!</h1>
                        <Container className="center hero-col">
                            <Button label="Get started now!" />
                        </Container>
                    </div>
                </Col>
            </Row>
        </Container>
    )
}

export default HomeView;