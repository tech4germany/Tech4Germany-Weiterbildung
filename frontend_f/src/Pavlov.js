import React from 'react';
import { Option } from './Option';
// Material
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

export class Pavlov extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			options: [],
			uuid: ''
		};
		this.handleClick = this.handleClick.bind(this);
	}

	componentDidMount() {
		fetch('http://0.0.0.0:3001/init').then(res => res.json())
		.then((data => this.setState({
				uuid: data.uuid,
				options: data.options
			})
		));
	}

	handleClick(title) {
		fetch('http://0.0.0.0:3001/select', {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.state.uuid,
				option: title
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		})
		.then(res => res.json()).then((data => this.setState({options: data.options})));
	}

	render() {
		return (
			<Grid container spacing={6}>
				<Grid item xs={12} justify="center">
					<Typography variant="h4" component="h3" gutterBottom>
						Was interessiert Dich mehr?
					</Typography>
				</Grid>
				{this.state.options.map(title => <Option title={title} onClick={this.handleClick} />)}
			</Grid>
		);
	}
}