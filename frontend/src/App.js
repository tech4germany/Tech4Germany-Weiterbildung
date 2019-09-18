import React from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom'
import CardPage from './pages/CardPage'
import CheckPage from './pages/CheckPage'
import ListPage from './pages/ListPage'

export default function App() {
    return (

        <Switch>
            <Route exact path="/" component={CardPage} />
            <Route exact path="/check" component={CheckPage} />
            <Route exact path="/list" component={ListPage} />
        </Switch>
    )
}
