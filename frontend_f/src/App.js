import React from 'react';
import { Pavlov } from './Pavlov';
import Typography from '@material-ui/core/Typography';

export class App extends React.Component {
  render() {
    return (
      <div>
        <Typography variant="h1" component="h2" gutterBottom>
          Pavlov is here to help
        </Typography>
        <Pavlov />
      </div>
    );
  }
}