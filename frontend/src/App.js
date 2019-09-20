import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom'
import CardPage from './pages/CardPage'
import CheckPage from './pages/CheckPage'
import CourseList from './pages/CourseList'
import JobView from './pages/JobView'
import CourseView from "./pages/CourseView";

class App extends Component {
    constructor(props) {
        super(props);
        this.target_job_selection_handler = this.target_job_selection_handler.bind(this);
        this.goal_selection_handler = this.goal_selection_handler.bind(this);
        this.course_selection_handler = this.course_selection_handler.bind(this);
        this.state = {
            question_id: 1,
            target_job : '',
            goal: '',
            course: ''
        };
    }

    target_job_selection_handler(option) {
        this.setState({question_id: this.state.question_id + 1, target_job: option, goal: this.state.goal, course: this.state.course});
    }

    goal_selection_handler(option) {
        this.setState({question_id: this.state.question_id + 1, target_job: this.state.target_job, goal: option, course: this.state.course});
    }

    course_selection_handler(id) {
        this.setState({question_id: this.state.question_id + 1, target_job: this.state.target_job, goal: this.state.goal, course: id});
    }

    render() {
        return (

            <Switch>
                <Route exact path="/"
                       render = {(props) => <CardPage {...props} option_handler={this.target_job_selection_handler}/>}/>
                <Route exact path="/check"
                       render = {(props) => <CheckPage {...props} option_handler={this.goal_selection_handler}/>}/>
                <Route exact path="/jobs"
                        render = {(props) => <JobView {...props} job={this.state.target_job} goal={this.state.goal}/>}/>
                <Route exact path="/list"
                       render = {(props) => <CourseList {...props} course_handler={this.course_selection_handler} job={this.state.target_job} goal={this.state.goal}/>}/>
                <Route exact path="/course"
                       render = {(props) => <CourseView {...props} course={this.state.course}/>}/>
            </Switch>
        )
    }
}

export default App;
