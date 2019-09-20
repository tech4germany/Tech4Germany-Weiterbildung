import Container from '@material-ui/core/Container';
import React from "react";
import Button from "@material-ui/core/Button";
import {Link} from "react-router-dom";
import {makeStyles} from "@material-ui/core";

const useStyles = makeStyles(theme => ({
    formControl: {
        margin: theme.spacing(3),
    },
}));

const JobView = props => {
    const classes = useStyles();
    const [value, setValue] = React.useState('female');

    function handleChange(event) {
        setValue(event.target.value);
    }

    return (
        <Container>
            <p>Dein Job: {props.job}</p>
            <p>Dein Ziel: {props.goal}</p>
            <Link to="/list"><Button variant="contained" color="primary" className={classes.button}>
                Kurse anzeigen
            </Button></Link>
        </Container>
    )

}

export default JobView;