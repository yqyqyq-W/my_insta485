import React from 'react';
import PropTypes from 'prop-types';
import Posts from './posts';
import Post from './post';
import InfiniteScroll from "react-infinite-scroll-component";

class Index extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      nextPage: '',
      items: [],
    };
    this.url = "/api/v1/p/";
    this.fetchData = this.fetchData.bind(this);
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
          nextPage: data.next,
          items: data.results,
        });
      })
      .catch((error) => console.log(error));
  }


function fetchData(){
    fetch(state.nextPage, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(
          () => ({
            nextPage: data.next,
            items: state.items.concat(data.results)
          }),
        );
      })
      .catch((error) => console.log(error));
  }


  // TODO: response time
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    let hasMore = state.nextPage !== '';
    return (
      // TODO:infinite scroll
      <div>
        <InfiniteScroll
        dataLength={state.items.length} //This is important field to render the next data
        next={state.fetchData}
        hasMore={hasMore}
        loader={<h3>Loading...</h3>}
        endMessage={
            <p>
                <b>Yay! You have seen it all</b>
            </p>
        }
        >

        {state.items.map((item) => (
          <Post url={item.url} key={item.postid} />
        ))}

        </InfiniteScroll>
      </div>
    );
  }

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
