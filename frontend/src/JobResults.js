import React from 'react';
// material
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import CircularProgress from '@material-ui/core/CircularProgress';

export class JobResults extends React.Component {
	hasJobs() {
		if (typeof this.props.jobs !== 'undefined' && this.props.jobs.length > 0 && this.props.counter > 3) {
			return true;
		} else {
			return false;
		}
	}



	render() {
		if (!this.hasJobs()) {
			return(
				<Typography variant="h5" component="h4" style={{ marginTop: 60, marginBottom: 20 }}>
					Gib mehr Präferenzen an, um deine Berufe zu sehen!
				</Typography>
			);
		} else {
			return(
				<React.Fragment>
					<Typography variant="h5" component="h4" style={{ marginTop: 40 }}>
						Deine Top Berufe:
					</Typography>
					<List dense={true} component="nav" aria-label="main mailbox folders">
						{this.props.jobs.map(job => 
							<ListItem key={job}
									  button>
			          <ListItemText primary={job} />
			        </ListItem>
						)}
		      </List>
		    </React.Fragment>
		  );
	  }
	}
}