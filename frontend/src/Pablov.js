import React from 'react';
import { Option } from './Option';
import { Submit } from './Submit';
import { JobResults } from './JobResults';
// Material
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

export class Pablov extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			uuid: '',
			options: [], //['Wirtschaft, Verwaltung', 'Gesundheit', 'Kunst, Kultur, Gestaltung', 'Landwirtschaft, Natur', 'Metall, Maschinenbau', 'IT, Computer', 'Naturwissenschaften', 'Malen nach Zahlen'],
			optionsType : 'Branche',
			selected: [],
			jobs: [],
			jobsCounter: 0,
			liked: []
		};
		this.selectOption = this.selectOption.bind(this);
		this.sendSelections = this.sendSelections.bind(this);
	}

	componentDidMount() {
		fetch(new URL('init', process.env.REACT_APP_API_URL)).then(res => res.json())
		.then((data => this.setState({
				uuid: data.uuid,
				options: data.options,
				optionsType: data.option_type,
				liked: data.fav_jobs
			})
		));
	}

	selectOption(id) {
		if (this.hasMultiOptions()) {
			if (!this.state.selected.includes(id)) {
				this.setState({
					selected: this.state.selected.concat(id)
				});
			}
			else {
				this.setState({
					selected: this.state.selected.filter(function(option) {
						return option !== id
					})
				});
			}
		} else {
			this.setState({
				selected: [id]
			}, () => {
				this.sendSelections();
			});
		}
	}

	sendSelections() {
		this.increaseJobsCounter();
		fetch(new URL('select', process.env.REACT_APP_API_URL), {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.state.uuid,
				options: this.state.selected,
				option_type: this.state.optionsType
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		})
		.then(res => res.json())
		.then((data => this.setState({
			options: data.options,
			jobs: data.jobs,
			optionsType: data.option_type,
			fav_jobs: data.fav_jobs,
			// shows jobs after response:
			jobsCounter: this.state.jobsCounter > 3 ? 5 : this.state.jobsCounter 
		})));

	}

	hasMultiOptions() {
		if (this.state.options.length > 2) {
			return true;
		} else {
			return false;
		}
	}

	increaseJobsCounter() {
		this.setState({
			jobsCounter: this.state.jobsCounter + 1 
		});
	}

	render() {
		const gridM = this.state.options.length > 2 ? 3 : 6;

		return (
			<React.Fragment>
				<Grid container spacing={2}  justify="center">
					<Grid item xs={12}>
						{this.state.options.length > 0 && <Typography variant="h4" gutterBottom>
							Was interessiert Dich mehr?
						</Typography>}
					</Grid>
					{this.state.options.map(option => 
						<Option
							key={option.id.$oid}
							id={option.id.$oid}
							title={option.title}
							info={option.info} 
							type={this.state.optionsType} 
							gridM={gridM} 
							onClick={this.selectOption}
							uuid={this.state.uuid}
						/>
					)}
				</Grid>
				{this.hasMultiOptions() && this.state.selected.length > 0 && <Submit onClick={this.sendSelections}/>}
				<JobResults 
					jobs={this.state.jobs} 
					counter={this.state.jobsCounter}
					fav_jobs={this.state.fav_jobs}
					uuid={this.state.uuid}
					type={this.state.optionsType}
				/>
			</React.Fragment>
		);
	}
}