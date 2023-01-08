import React, { Component } from 'react'
import { Form, TextArea, Button } from 'semantic-ui-react'
import { HandleCardContext, handleCardHeader} from './Card.js'
// import fetch from 'node-fetch';
// console.log(`data: ${JSON.stringify(markets)}`)


export default class BulkSearch extends Component {
  state = {
    payload: null,
    activeButton: 'bulkSearch',
    loading: false,
    bulk_search_text: '',
    post_search: false,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  set_bulk_search = () => {
    this.setState({ activeButton: 'bulkSearch' });
  }

  set_file_search = () => {
    this.setState({ activeButton: 'fileSearch' });
  }

  set_text_value = (event) => {
    this.setState({bulk_search_text: event.target.value});
  }

  process_text = async (e) => {
    e.preventDefault();
    if (this.state.bulk_search_text !== '') {
      // console.log(`data: ${JSON.stringify(this.state.bulk_search_text)}`)
      var cleaned = (this.state.bulk_search_text.replace(/\n/g,',')).trim();
      console.log(`Searching for: ${JSON.stringify(cleaned)}`)

      const params = new URLSearchParams();
      params.append('domains', cleaned);

      const response = await fetch('http://127.0.0.1:5000/api/v1/bulkSearch', {method: 'POST', body: params});
      const search_results = await response.json();

      console.log(`Search results: ${JSON.stringify(search_results)}`)
    } else {
      console.log("text is '' yo!")
    }
  }

  clear_search_text = () => {
    this.setState({bulk_search_text: ''});
  }


  render() {
    return (
      <div className="BulkSearch" id="bulksearch" class="ui hidden section divider">
        
      <Button.Group fluid>
        <Button
          onClick={this.set_bulk_search}
          positive={this.state.activeButton === 'bulkSearch'}>Bulk Search
        </Button>
        
        <Button.Or />

        <Button
          secondary
          onClick={this.set_file_search}
          positive={this.state.activeButton === 'fileSearch'}>Load from File
        </Button>
      </Button.Group>

      <div class="ui hidden section divider"></div>

      {
        this.state.activeButton === 'bulkSearch' ? (

          <Form class="ui form">
            <TextArea
              placeholder='Enter one ENS domain per line'
              style={{'backgroundColor':'black', 'color':'white', minHeight: 500}}
              type="text"
              value={this.state.bulk_search_text}
              defaultValue={this.state.bulk_search_text}
              onChange={ (event) => {
                this.set_text_value(event)
              }}
            />

            <Button.Group fluid>
              <Button
                primary
                onClick={this.process_text}
                loading={this.state.loading}>search
              </Button>
              
              <Button
                secondary
                onClick={this.clear_search_text}>
                clear
              </Button>
            </Button.Group>
          </Form>
        ) : (<div/>)
      }
    </div>
    )
  }
}