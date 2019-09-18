import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { FixedSizeList } from 'react-window';
import Paper from '@material-ui/core/Paper';
import Container from '@material-ui/core/Container';
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
        height: 400,
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
}));

_renderTodos(){
    return this.state.todos.map(el => {
        return <ListItem primaryText={el.text} key={el.id}/>
    })
}

function Row(props) {
    const { index, style } = props;

    return (
        <ListItem button style={style} key={index}>
            <ListItemText primary={`Kurs ${index + 1}`} />
        </ListItem>
    );
}

Row.propTypes = {
    index: PropTypes.number.isRequired,
    style: PropTypes.object.isRequired,
};

export default function VirtualizedList() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Container>
                <Paper>
                    <Typography variant="h5" component="h3">
                        This is a sheet of paper.
                    </Typography>
                </Paper>
                <FixedSizeList height={1200} width={360} itemSize={46} itemCount={200}>
                    {Row}
                </FixedSizeList>
            </Container>
        </div>
    );
}