import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import { red } from '@material-ui/core/colors';
import { Link } from 'react-router-dom'

const useStyles = makeStyles(theme => ({
    card: {
        maxWidth: 1000,
    },
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    select: {

    },
    avatar: {
        backgroundColor: red[500],
    },
}));

const JobCard = props => {
    const classes = useStyles();

    return (
        <Card className={classes.card}>
            <CardHeader
                title={props.title}
            />
            <CardMedia
                className={classes.media}
                image={props.image_source}
                title={props.title}
            />
            <CardContent>
                <Typography variant="body2" color="textSecondary" component="p">
                    {props.description}
                </Typography>
            </CardContent>
            <CardActions style={{justifyContent: 'center'}}>
                <Link to="/check"><Button variant="contained" color="primary" className={classes.button}>
                Auswählen
                </Button></Link>
        </CardActions>
        </Card>
    );
}

export default JobCard;