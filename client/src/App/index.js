import React from 'react';
import {Route, Link} from 'react-router-dom';

import IndexPage from '../IndexPage';
import AboutPage from '../AboutPage';
import Header from '../components/layout/Header';


class App extends React.Component {
    render() {
        return (
            <div className="App">
                <Header />
                <header>
                    <Link to="/home">Home</Link>
                    <Link to="/about-us">About us</Link>
                </header>

                <Route exact path="/" component={IndexPage}/>
                <Route exact path="/about-us" component={AboutPage}/>
            </div>
        );
    }
}

export default App;
