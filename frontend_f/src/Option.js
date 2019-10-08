import React from 'react';
// Material
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardActionArea from '@material-ui/core/CardActionArea';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

export class Option extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
		const title = this.props.title;
		this.props.onClick(title)
	}

	render() {
		const title = this.props.title[0].toUpperCase() + this.props.title.slice(1)

		return (
			<Grid item xs={12} sm={6} md={this.props.gridM}>
				<Card>
					<CardActionArea onClick={this.handleClick}>
						<CardContent style={{ minHeight: 140 }}>
							<Typography color="textSecondary" gutterBottom>
		          	{this.props.type}
		        	</Typography>
		        	<Typography variant="h4" component="h2" style={{ overflowWrap: 'break-word' }}>
			          {title}
			        </Typography>
			        <Typography variant="body2" component="p">
			          Haben wir noch mehr Infos?
			        </Typography>
			    	</CardContent>
			    </CardActionArea>
					<CardActions>
		        <Button size="small">Merken</Button>
		        <Button size="small">Mehr Infos</Button>
		      </CardActions>
				</Card>
			</Grid>
		);
	}
}