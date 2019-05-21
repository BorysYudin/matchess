import React from 'react';
import {Route, Link} from 'react-router-dom';

import Home from '../Home';
import About from '../About';
import Header from '../components/layout/Header';


class App extends React.Component {
    render() {
        return (
            <div className="App">
                <Header />
                <header>
                    <Link to="/">Home</Link>
                    <Link to="/about-us">About us</Link>
                </header>

                <Route exact path="/" component={Home}/>
                <Route exact path="/about-us" component={About}/>
            </div>
        );
    }
}

export default App;
