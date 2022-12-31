import React, { Component } from 'react'
import { Form, TextArea, Header, Button } from 'semantic-ui-react'
import {_Card, HandleCardContext, handleCardHeader} from './Card.js'
// console.log(`data: ${JSON.stringify(markets)}`)


export default class BulkSearch extends Component {
  state = {
    payload: null,
    activeButton: 'bulkSearch',
    loading: false,
    bulk_search_text: null,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  handle_bulk_search = () => {
    this.setState({ activeButton: 'bulkSearch' });
  }

  handle_file_search = () => {
    this.setState({ activeButton: 'fileSearch' });
  }

  text_value = (event) => {
    if (event.target.value === "") {
      this.setState({bulk_search_text: null});
    } else {
      this.setState({bulk_search_text: event.target.value});
    }
  }

  process_text = () => {
    if (this.state.bulk_search_text !== null) {
      // console.log(`data: ${JSON.stringify(this.state.bulk_search_text)}`)

      var cleaned = (this.state.bulk_search_text.replace(/\n/g,',')).trim();

      console.log(`data: ${JSON.stringify(cleaned)}`)
      // data: "lobo\ntoro\ntest" LOOKS LIKE THIS
      // 2453,5674,23426,1235,lobo SEND LIKE THIS

      // http://127.0.0.1:5000/api/v1/bulkSearch
    } else {
      console.log("text is null yo!")
    }
  }

  render() {
    return (
      <div className="BulkSearch" id="bulksearch" class="ui hidden section divider">
        
      <Button.Group fluid>
        <Button
          onClick={this.handle_bulk_search}
          positive={this.state.activeButton == 'bulkSearch'}>Bulk Search
        </Button>
        
        <Button.Or />

        <Button
          onClick={this.handle_file_search}
          positive={this.state.activeButton == 'fileSearch'}>Load from File
        </Button>
      </Button.Group>

      <div class="ui hidden section divider"></div>

      {
        this.state.activeButton === 'bulkSearch' ? (
          <Form>
            <TextArea
              placeholder='Enter one ENS domain per line'
              style={{'backgroundColor':'black', 'color':'white'}}
              type="text"
              value={this.state.bulk_search_text}
              onChange={ (event) => {
                this.text_value(event)
              }}
            />
          </Form>
        ) : (<div/>)
      }

      <div class="ui hidden section divider"></div>

      <div>
      <Button.Group fluid>
        <Button
          onClick={this.process_text}
          loading={this.state.loading}>search
        </Button>
        <Button>
          Clear
        </Button>
        </Button.Group>
      </div>

    </div>
    )
  }
}