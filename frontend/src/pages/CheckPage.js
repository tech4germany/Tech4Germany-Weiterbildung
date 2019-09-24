import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import {Link} from "react-router-dom";
import CardPage from "./CardPage";
import Header from "../modals/Header";

const useStyles = makeStyles(theme => ({
    formControl: {
        margin: theme.spacing(3),
    },
}));

const CheckPage = props => {
    const classes = useStyles();
    const [value, setValue] = React.useState('female');

    function handleChange(event) {
        setValue(event.target.value);
    }

    return (
        <Grid container spacing={3}
              justify="center"
              alignItems="center">
            <Header/>
            <Grid item xs={12}>
                <FormControl component="fieldset" className={classes.formControl}>
                    <FormLabel component="legend">Was trifft am ehesten auf dich zu?</FormLabel>
                    <RadioGroup aria-label="goal" name="goal" value={value} onChange={handleChange}>
                        <FormControlLabel value="ball" control={<Radio />} label="Ich möchte am Ball bleiben." />
                        <FormControlLabel value="wechseln" control={<Radio />} label="Ich möchte in eine andere Branche wechseln." />
                        <FormControlLabel value="spezialisieren" control={<Radio />} label="Ich möchte mich in meiner Branche spezialisieren." />
                    </RadioGroup>
                    <Link to="/jobs"><Button variant="contained" color="primary" className={classes.button} onClick={() => props.option_handler(value)}>
                        Weiter
                    </Button></Link>
                </FormControl>
            </Grid>
        </Grid>
    );
}

export default CheckPage;