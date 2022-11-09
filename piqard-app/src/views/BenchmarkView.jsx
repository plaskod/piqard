import { useState } from "react";
import { Container } from "react-bootstrap";
import LoadBenchmark from "../components/benchmarks/LoadBenchmark";
import QuestionsList from "../components/benchmarks/QuestionsList";
import ScoresComponent from "../components/benchmarks/ScoresComponent";

import './BenchmarkView.css'

function BenchmarkView(){
    const [benchmark, setBenchmark] = useState({scores:[], report:[]});

    function handleSetBenchmark(event){
        const fileReader = new FileReader();
        fileReader.readAsText(event.target.files[0], "UTF-8");
        fileReader.onload = e => {
            const loadedBenchmark = JSON.parse(e.target.result)
            setBenchmark(loadedBenchmark);
          };
    }

    return(
        <Container fluid className="benchmark-view-container">
            <LoadBenchmark handleSetBenchmark={handleSetBenchmark}/>
            <ScoresComponent scores={benchmark.scores}/>
            {benchmark && (
                <QuestionsList questions={benchmark.report}/> 
            )}
        </Container>
    )
}

export default BenchmarkView;