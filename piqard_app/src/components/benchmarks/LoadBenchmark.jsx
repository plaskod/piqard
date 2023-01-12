import React from "react";
import { Form } from "react-bootstrap";

import './LoadBenchmark.css'


function LoadBenchmark({handleSetBenchmark}){
    return(
        <Form.Group controlId="formFile" className="mb-3 load-benchmark">
            <Form.Label>Load benchmark report file</Form.Label>
            <Form.Control type="file" onChange={(e) => {handleSetBenchmark(e)}}/>
        </Form.Group>
    )
}


export default LoadBenchmark;