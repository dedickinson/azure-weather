// @flow

import * as React from 'react';
import { Jumbotron, Button } from 'react-bootstrap';
//import logo from './logo.svg';
import './App.css';

type Props = {
  title: String,
};

type State = {};

class App extends React.Component<Props, State> {
  static defaultProps = {
    title: 'Cloud Weather',
  };
  state = {};

  componentDidMount() {}

  render() {
    return (
      <div className="App">
        <Jumbotron>
          <h1>{this.props.title}</h1>
          <p>
            This is a simple hero unit, a simple jumbotron-style component for calling
            extra attention to featured content or information.
          </p>
          <p>
            <Button bsStyle="primary">Learn more</Button>
          </p>
        </Jumbotron>
      </div>
    );
  }
}

export default App;
