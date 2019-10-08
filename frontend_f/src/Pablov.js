import React from 'react';
import { Option } from './Option';
import { Submit } from './Submit';
// Material
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

export class Pablov extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			options: [], //['Wirtschaft, Verwaltung', 'Gesundheit', 'Kunst, Kultur, Gestaltung', 'Landwirtschaft, Natur, Umwelt', 'Metall, Maschinenbau', 'IT, Computer', 'Naturwissenschaften'],
			optionsCategory : 'Bereiche',
			selected: [],
			uuid: ''
		};
		this.selectOption = this.selectOption.bind(this);
		this.sendSelections = this.sendSelections.bind(this);
	}

	componentDidMount() {
		fetch('http://0.0.0.0:3001/init').then(res => res.json())
		.then((data => this.setState({
				uuid: data.uuid,
				options: data.options
			})
		));
	}

	// does not deselect 
	selectOption(title) {
		if (this.hasMultiOptions()) {
			if (!this.state.selected.includes(title)) {
				this.setState({
					selected: this.state.selected.concat(title)	
				});
			}
		} else {
			this.sendSelections(title);
		}
	}

	sendSelections(titles) {
		fetch('http://0.0.0.0:3001/select', {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.state.uuid,
				option: titles
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		})
		.then(res => res.json()).then((data => this.setState({options: data.options})));
	}

	hasMultiOptions() {
		if (this.state.options.length > 2) {
			return true;
		} else {
			return false;
		}
	}

	render() {
		const gridM = this.state.options.length > 2 ? 3 : 6;
		const type = this.state.options.length > 2 ? 'multi' : 'dual';

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
							category={this.state.optionsCategory} 
							gridM={gridM} 
							onClick={this.selectOption}
							type={type}
						/>
					)}
				</Grid>
				{this.hasMultiOptions() && <Submit onClick={this.sendSelections}/>}
			</React.Fragment>
		);
	}
}