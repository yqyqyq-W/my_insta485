import React from 'react';
import PropTypes from 'prop-types';
import Posts from './posts';

class Index extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    // console.log('index ctor');
    super(props);
    this.state = { postsUrl: '' };
    // if (performance.getEntriesByType('Navigation')[0].type === 'back_forward') {
    //   window.history.back();
    // }
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    // console.log('index start get url');
    const { url } = this.props;
    // console.log('index get url');
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        // console.log('index response');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('index setstate');
        this.setState({
          postsUrl: data.posts,
        });
        // const { postsUrl } = this.state;
        // window.history.pushState({ postsUrl }, '', url);
        // console.log('index setstate success');
      })
      .catch((error) => console.log(error));
  }

  // TODO: response time
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { postsUrl } = this.state;
    // Render number of post image and post owner
    // console.log(postsUrl);
    if (postsUrl === '') {
      return (
      // TODO:infinite scroll

        <h1>Loading</h1>);
    }
    return (
      <div>
        <Posts url={postsUrl} />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
