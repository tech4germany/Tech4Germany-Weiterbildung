import React from 'react';
// material
import Button from '@material-ui/core/Button';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import StarIcon from '@material-ui/icons/Star';

export class LikeButton extends React.Component{
	constructor(props) {
		super(props);
		this.state = {
			liked: false
		};
		this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
		if(!this.state.liked) {
			this.send_like();
		}
		else {
			this.send_unlike();
		}
		this.setState({
			liked: !this.state.liked
		})
	}

	send_like() {
		fetch(new URL('like', process.env.REACT_APP_API_URL), {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.props.uuid,
				options: this.props.title,
				option_type: this.props.type
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	send_unlike() {
		fetch(new URL('unlike', process.env.REACT_APP_API_URL), {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.props.uuid,
				options: this.props.title,
				option_type: this.props.type
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	render() {
		return(
			<Button size="small" onClick={this.handleClick}>
				{this.state.liked ? <StarIcon color={"primary"}/> : <StarBorderIcon/>} 
				Merken
			</Button>
		);
	}
}