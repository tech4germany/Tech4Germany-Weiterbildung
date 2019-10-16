import React from 'react';
import { LikeButton } from './LikeButton';
// material
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import LinearProgress from '@material-ui/core/LinearProgress';
import StarIcon from '@material-ui/icons/Star';

export class JobResults extends React.Component {
	hasJobs() {
		if (typeof this.props.jobs !== 'undefined' && this.props.jobs.length > 0 && this.props.counter > 4) {
			return true;
		} else {
			return false;
		}
	}

	render() {
		if (!this.hasJobs()) {
			return(
				<React.Fragment>
					<Typography variant="h5" component="h4" style={{ marginTop: 60, marginBottom: 20 }}>
						Gib mehr Präferenzen an, um Deine Berufe zu sehen!
					</Typography>
					<LinearProgress variant="determinate" value={this.props.counter * 25} style={{ maxWidth: 600, height: 6 }}/>
				</React.Fragment>
			);
		} else {
			return(
				<React.Fragment>
					<Typography variant="h4" style={{ marginTop: 40 }}>
						Deine Top Berufe:
					</Typography>
					<List dense={true} component="nav" aria-label="main mailbox folders">
						{this.props.jobs.map(job => 
							<ListItem key={job} button>
			          <ListItemText primary={<Typography variant="body1">{job}</Typography>}/>
			          <LikeButton 
			          	onClick={this.props.likeHandler}
			          	id={job.id}
			          />
			        </ListItem>
						)}
		      </List>
		    </React.Fragment>
		  );
	  }
	}
}