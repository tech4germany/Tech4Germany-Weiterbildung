import React from 'react';
import { Pablov } from './Pablov';
import Typography from '@material-ui/core/Typography';

export class App extends React.Component {
  render() {
    return (
      <div style={{ padding: 10, position: 'relative', maxWidth: 1200 }}>
        <Typography variant="h1" component="h2" gutterBottom style={{ transform: 'rotate(-1deg)' }}>
          <span style={{ backgroundColor: '#6DECAF' }}>Pablov</span> is here to help!
        </Typography>
        <Pablov />
      </div>
    );
  }
}
