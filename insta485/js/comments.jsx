import React from 'react';
import PropTypes from 'prop-types';

/*
 Example:
    {
  "comments": [
    {
      "commentid": 1,
      "owner": "awdeorio",
      "owner_show_url": "/u/awdeorio/",
      "postid": 3,
      "text": "#chickensofinstagram"
    },
    {
      "commentid": 2,
      "owner": "jflinn",
      "owner_show_url": "/u/jflinn/",
      "postid": 3,
      "text": "I <3 chickens"
    },
    {
      "commentid": 3,
      "owner": "michjc",
      "owner_show_url": "/u/michjc/",
      "postid": 3,
      "text": "Cute overload!"
    }
  ],
  "url": "/api/v1/p/3/comments/"
} */
class Comments extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { comments: [], length: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
          length: data.comments.length,
        });
      })
      .catch((error) => console.log(error));
  }

  getComment(index) {
    const { comments } = this.state;
    return (
      <div>
        <a className="t" href={comments[index].owner_show_url}>{comments[index].owner}</a>
        <p>{ comments[index].text }</p>
        <br />
        <br />
      </div>
    );
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { length } = this.state;

    let tmp;
    if (!length) {
      let i = 0;
      for (; i < length; i += 1) {
        tmp.append(this.getComment(i));
      }
    }
    // TODO:add comment update html
    tmp.append(<div />);
    return (
      <div>
        { tmp }
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
