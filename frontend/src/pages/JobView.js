import Container from '@material-ui/core/Container';
import React from "react";
import Button from "@material-ui/core/Button";
import {Link} from "react-router-dom";
import {makeStyles} from "@material-ui/core";
import Header from "../modals/Header";
import Grid from "@material-ui/core/Grid";

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
        <Grid container spacing={3}
              justify="center"
              alignItems="center">>
            <Header/>
            <Grid item xs={12}>
                <p>Dein Job: {props.job}</p>
                <p>Dein Ziel: {props.goal}</p>
                <Link to="/list"><Button variant="contained" color="primary" className={classes.button}>
                    Kurse anzeigen
                </Button></Link>
            </Grid>
        </Grid>
    )

}

export default JobView;