import React from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { About } from './components/About';
import { Users } from './components/Users';
import { Navbar } from './components/Navbar';
import { Recognition} from './components/Recognition';

function App() {
  return (
    <Router>
      <Navbar/>
      <div>
        <Switch>
          <Route path="/recog" component={Recognition}/>
          <Route path="/about" component={About}/>
          <Route path="/" component={Users}/>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
