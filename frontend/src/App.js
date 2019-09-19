import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom'
import CardPage from './pages/CardPage'
import CheckPage from './pages/CheckPage'
import CourseList from './pages/CourseList'

class App extends Component {
    constructor(props) {
        super(props);
        this.target_job_selection_handler = this.target_job_selection_handler.bind(this);
        this.goal_selection_handler = this.goal_selection_handler.bind(this);
        this.state = {
            question_id: 1,
            target_job : '',
            goal: ''
        };
    }

    target_job_selection_handler(option) {
        this.setState({question_id: this.state.question_id + 1, target_job: option, goal: this.state.goal});
    }

    goal_selection_handler(option) {
        this.setState({question_id: this.state.question_id + 1, target_job: this.state.target_job, goal: option});
    }

    render() {
        return (

            <Switch>
                <Route exact path="/"
                       render = {(props) => <CardPage {...props} option_handler={this.target_job_selection_handler}/>}/>
                <Route exact path="/check"
                       render = {(props) => <CheckPage {...props} option_handler={this.goal_selection_handler}/>}/>
                <Route exact path="/list"
                       render = {(props) => <CourseList {...props} option_handler={this.goal_selection_handler}/>}/>
            </Switch>
        )
    }
}

export default App;
