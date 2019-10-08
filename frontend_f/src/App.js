import React from 'react';
import { Pablov } from './Pablov';
import Typography from '@material-ui/core/Typography';

export class App extends React.Component {
  render() {
    return (
      <div style={{ padding: 10, position: 'relative' }}>
        <Typography variant="h1" component="h2" gutterBottom>
          <em style={{ backgroundColor: '#6DECAF' }}>Pablov</em> is here to help
        </Typography>
        <Pablov />
      </div>
    );
  }
}