import React from 'react';
// material
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';

export class JobResults extends React.Component {
	render() {
		return (
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
		)
	}
}