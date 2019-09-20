import React from "react";
import {Link} from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import Container from "@material-ui/core/Container";

class CourseView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
    }

    componentDidMount() {
        fetch(`http://bmas-backend.gn38mxa6rg.us-east-2.elasticbeanstalk.com/courses/find/${this.props.course}`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result
                    });
                },
                // Note: it's important to handle errors here
                // instead of a catch() block so that we don't swallow
                // exceptions from actual bugs in components.
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    render() {
        const { error, isLoaded, items } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <Container><CircularProgress/></Container>
        } else {
            return (
                <Container>
                    <p>Course Title: {items.title}</p>
                    <p>Course parent 1: {items.parent_1}</p>
                    <p>Course parent 2: {items.parent_2}</p>
                </Container>
            );
        }
    }
}

export default CourseView;