import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
// import Posts from './posts';
import Post from './post';

class Index extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    // console.log('index ctor');
    super(props);
    this.state = {
      hasMore: true,
      numPage: 0,
      numPost: 0,
    };
    this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    // const { url } = this.props;
   this.fetchData();
  }

  fetchData() {
    const { numPage, numPost, hasMore } = this.state;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        // console.log('index response');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('index setstate');
        this.setState({
          hasMore: data.next !== '',
          numPage: numPage + 1,
          numPost: numPost + data.results.length,
        });
        // console.log('index setstate success');
        window.history.pushState(this.state, null, null);
      })
      .catch((error) => console.log(error));
  }

  // TODO: response time
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { hasMore, numPost } = this.state;
    // Render number of post image and post owner
    // console.log(postsUrl);
    // if (postsUrl === '') {
    //   return (
    //   // TODO:infinite scroll
    //
    //     <h1>Loading</h1>);
    // }
    // return (
    //   <div>
    //     <Posts url={postsUrl} />
    //   </div>
    // );
    return (
      <div>
        <InfiniteScroll
          dataLength={numPost} // This is important field to render the next data
          next={this.fetchData}
          hasMore={hasMore}
          loader={<h4>Loading...</h4>}
          endMessage={(
            <p>
              <b>Yay! You have seen it all</b>
            </p>
          )}
        >

        <Posts length={numPost} />

        </InfiniteScroll>
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
