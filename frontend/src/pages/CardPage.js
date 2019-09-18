import Container from '@material-ui/core/Container';
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import JobCard from "../modals/JobCard";
import React from "react";

const CardPage = props =>  {
    return (
        <Container>
            <Grid container spacing={3}
                  justify="center"
                  alignItems="center">
                <Grid item xs={12}>
                    <Box><h1>Was gefällt dir besser?</h1></Box>
                </Grid>
                <Grid item xs={6}>
                    <JobCard title={'Schweißen'} image_source={'./job_images/schweißen.jpg'} description={'Geprüfte Schweißer/innen verbinden Metallteile und montieren Anlagen- und Konstruktionsbauteile mittels unterschiedlicher Schweißverfahren.'} option_handler={props.option_handler}/>
                </Grid>
                <Grid item xs={6}>
                    <JobCard title={'Töpfern'} image_source={'./job_images/töpfern.jpg'} description={'Keramiker/innen stellen Gebrauchskeramik, Baukeramik und Zierkeramik her. Ihre Aufgaben reichen von Planung und Entwurf über die Fertigung bis hin zum Verkauf.'}/>
                </Grid>
            </Grid>
        </Container>
    )
}

export default CardPage;