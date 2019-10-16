import React from 'react';
import { LikeButton } from './LikeButton'
// Material
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardActionArea from '@material-ui/core/CardActionArea';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

export class Option extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			selected: false
		};
		this.handleClick = this.handleClick.bind(this);
	}

	componentDidMount() {
		this.setState({
			selected: false,
		});
	}

	handleClick() {
		const title = this.props.title;
		this.props.onClick(title);
		this.setState({
			selected: !this.state.selected
		});
	}

	reduceToFirstSentence(string) {
		if (string.length > 0) {
			if(string.indexOf('.') != -1) {
				string = string.replace(/bzw\./, "beziehungsweise");
				string = string.replace(/z\.B\./, "zum Beispiel");
				var sentence = string.match(/[^\.!?]+[\.!?]+/)[0];
				sentence = sentence.length > 200 ? (sentence.slice(0,200) + '...') : sentence;
				return sentence;
			}
			else {
				return string.length > 200 ? (string.slice(0,200) + '...') : string;
			}
		} 
	}

	render() {
		const title = this.props.title.title[0].toUpperCase() + this.props.title.title.slice(1)
		const info = this.reduceToFirstSentence(this.props.title.info)

		return (
			<Grid item xs={12} sm={6} md={this.props.gridM}>
				<Card style={{ backgroundColor: this.state.selected ? '#6DECAF' : 'white' }}>
					<CardActionArea onClick={this.handleClick}>
						<CardContent style={{ minHeight: 200 }}>
							<Typography color="textSecondary" gutterBottom>
		          	{this.props.type}
		        	</Typography>
		        	<Typography variant="h4" component="h2" style={{ overflowWrap: 'break-word' }}>
			          {title}
			        </Typography>
			        <Typography variant="body2" component="p" style={{ marginTop: 10 }}>
			          {info}
			        </Typography>
			    	</CardContent>
			    </CardActionArea>
			    {this.props.type === 'Berufe' && 
						<CardActions>
							<LikeButton 
								onClick={this.likeOption}
								title={this.props.title}
								uuid={this.props.uuid}
								type={this.props.type}
							/>
			      </CardActions>
			    }
				</Card>
			</Grid>
		);
	}
}