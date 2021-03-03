import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

/*
 Example:
    {
  "next": "",
  "results": [
    {
      "postid": 3,
      "url": "/api/v1/p/3/"
    },
    {
      "postid": 2,
      "url": "/api/v1/p/2/"
    },
    {
      "postid": 1,
      "url": "/api/v1/p/1/"
    }
  ],
  "url": "/api/v1/p/"
} */
class Posts extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { posts: [], length: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          posts: data.results,
          length: data.results.length,
        });
      })
      .catch((error) => console.log(error));
  }

  static getPost(postid, link) {
    return (
      <div>
        <Post url={link} postid={postid} />
      </div>
    );
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { posts, length } = this.state;
    if (!length) {
      const { renderedPost } = this.getPost(posts[0].postid, posts[0].url);
      let i = 1;
      for (;i < posts.length; i += 1) {
        renderedPost.append(this.getPost(posts[i].postid, posts[i].url));
      }

      return (
        <div>
          { renderedPost }
        </div>
      );
    }

    return (<div />);
  }
}

Posts.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Posts;
