import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import Verification from './pages/Verification';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/analysis" component={Analysis} />
        <Route path="/verification" component={Verification} />
      </Switch>
    </Router>
  );
};

export default App;