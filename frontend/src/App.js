import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom'
import CardPage from './pages/CardPage'
import CheckPage from './pages/CheckPage'
import CourseList from './pages/CourseList'

class App extends Component {
    constructor(props) {
        super(props);
        this.option_handler = this.option_handler.bind(this);
        this.state = {
            question_id: 1
        };
    }

    option_handler(option) {
        console.log(this.state.question_id + 1);
        this.setState({question_id: this.state.question_id + 1});
    }

    render() {
        return (

            <Switch>
                <Route exact path="/"
                       render = {(props) => <CardPage {...props} option_handler={this.option_handler}/>}/>
                <Route exact path="/check"
                       render = {(props) => <CheckPage {...props} option_handler={this.option_handler}/>}/>
                <Route exact path="/list"
                       render = {(props) => <CourseList {...props} option_handler={this.option_handler}/>}/>
            </Switch>
        )
    }
}

export default App;
