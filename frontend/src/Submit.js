import React from 'react';
import Button from '@material-ui/core/Button';

export class Submit extends React.Component {
	handleClick = () => {
		this.props.onClick();
	}

	// hi

	render() {
		return(
			<Button 
				size="large" 
				color="primary" 
				onClick={this.handleClick}
				style={{ fontSize: '2em', position: 'absolute', right: 0, color: '#6DECAF' }}
			>
				Weiter
			</Button>
		)
	}
}
