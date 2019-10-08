import React from 'react';
import { Option } from './Option';
// Material
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

export class Pablov extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			options: ['Wirtschaft, Verwaltung', 'Gesundheit', 'Kunst, Kultur, Gestaltung', 'Landwirtschaft, Natur, Umwelt', 'Metall, Maschinenbau', 'IT, Computer', 'Naturwissenschaften'],
			optionsType : 'Bereiche',
			uuid: ''
		};
		this.handleClick = this.handleClick.bind(this);
	}

	// componentDidMount() {
	// 	fetch('http://0.0.0.0:3001/init').then(res => res.json())
	// 	.then((data => this.setState({
	// 			uuid: data.uuid,
	// 			options: data.options
	// 		})
	// 	));
	// }

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
		const gridM = this.state.options.length > 2 ? 3 : 6;

		return (
			<React.Fragment>
				<Grid container spacing={2}>
					<Grid item xs={12} justify="center">
						<Typography variant="h4" component="h3" gutterBottom>
							Was interessiert Dich mehr?
						</Typography>
					</Grid>
					{this.state.options.map(title => 
						<Option 
							title={title} 
							type={this.state.optionsType} 
							gridM={gridM} 
							onClick={this.handleClick} 
						/>
					)}
				</Grid>
				<Button size="big">Weiter</Button>
			</React.Fragment>
		);
	}
}