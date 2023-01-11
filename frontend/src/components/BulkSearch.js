import React, { Component } from 'react'
import axios from 'axios';
import { Form, TextArea, Button, Label, Tab, Card, Icon, Image, Rating} from 'semantic-ui-react'
import {
  handleStatus,
  handleName
}
from "../utils.js"
var async = require("async");
// import fetch from 'node-fetch';
// console.log(`data: ${JSON.stringify(markets)}`)


export default class BulkSearch extends Component {
  state = {
    payload: null,
    activeButton: 'fileSearch', // sets default landing page
    loading: false,
    bulk_search_text: '',
    bulk_search_results: null,
    file: null,
    fileName: null,
    liked: null,
    reverse_records: null,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  test = () => {
    console.log(`File: ${JSON.stringify(this.state.file)}`)
    console.log(`File name: ${JSON.stringify(this.state.fileName)}`)
  }

  set_bulk_search = () => {
    this.setState({ activeButton: 'bulkSearch' });
  }

  set_file_search = () => {
    this.setState({ activeButton: 'fileSearch' });
  }

  set_post_search =() => {
    this.setState({ activeButton: 'postSearch' });
  }

  set_text_value = (event) => {
    this.setState({bulk_search_text: event.target.value});
  }

  search = async (e) => {
    e.preventDefault();
    if (this.state.bulk_search_text !== '') {
      var cleaned = (this.state.bulk_search_text.replace(/\n/g,',')).trim();
      console.log(`[ACTION] Searching for: ${JSON.stringify(cleaned)} ...`)

      const params = new URLSearchParams();
      params.append('domains', cleaned);

      const response = await fetch('http://127.0.0.1:5000/api/v1/bulkSearch', {method: 'POST', body: params});
      const search_results = await response.json();

      let owners = null
      async.forEachOf(search_results.domains, (value, key, callback) => {
        if (value.owner !== undefined && value.owner !== null) {
          owners += value.owner + ','
        }
        callback();
      }, err => { if (err) console.error(err.message);}
      );

      await this.load_rr_data(owners)
      await this.setState({bulk_search_results: search_results})
      await this.setState({ activeButton: 'postSearch' });

      console.log(`[ACTION] State set to postSearch ...`)
    } else {
      console.log("text is ''")
    }
  }

  // Only resets on frontend if value is '' not null
  clear_search_text = () => {
    this.setState({bulk_search_text: ''});
  }

  load_rr_data = async (addresses) => {
    console.log(`[ACTION] Loading reverse records data ...`)
    const params = new URLSearchParams();
    params.append('addresses', addresses);

    const response = await fetch('http://127.0.0.1:5000/api/v1/getReverseRecords', {method: 'POST', body: params});
    const data = await response.json();
    await this.setState({ reverse_records: data.reverse_records });
    console.log(`[DATA] data: ${JSON.stringify(data.reverse_records)} ...`)
    console.log(`[ACTION] Set reverse records data ...`)
  }

  onFormSubmit = e => {
    e.preventDefault(); // Stop form submit
    console.log("[ACTION] Submitting form ...");
    this.fileUpload(this.state.file);
  };

  fileUpload = async file => {
    const formData = new FormData();
    // formData.append("file", file, {filename: this.state.fileName, contentType: 'text/plain'});
    formData.append("file", file, {filename: this.state.fileName, contentType: "multipart/form-data"});
    let response

    console.log(`Uploading file: ${JSON.stringify(file)}`)

    try {
      response = await fetch('http://127.0.0.1:5000/api/v1/handleSearchFile', {method: 'POST', body: formData});
    } catch (error) {
      console.error(Error(`Error uploading file ${error.message}`));
    }
    console.log(`fileupload Resp: ${JSON.stringify(response.json())}`)
  };

  fileChange = async e => {
    const reader = new FileReader()
    reader.onload = async (e) => { 
      const text = (e.target.result)
      console.log(`Text: ${text} ...`)
      alert(text)
      await this.setState(
        { file: text, fileName: e.target.files[0].name }
      );
    };
    reader.readAsText(e.target.files[0])

    // await this.setState(
    //   { file: text, fileName: e.target.files[0].name }
    // );
  };


  render() {
    return (
      <div className="BulkSearch" id="bulksearch" class="ui hidden section divider">
      {
        this.state.activeButton === 'bulkSearch' ? (
          <div>
          <Form class="ui form">
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
                onClick={this.search}
                loading={this.state.loading}>search
              </Button>
              
              <Button
                secondary
                onClick={this.clear_search_text}>
                clear
              </Button>
            </Button.Group>
          </Form>
          </div>
        ) : (<div></div>)
      }
      {
        this.state.activeButton === 'fileSearch' ? 
        (
          <div>
            <Tab.Pane attached={false} inverted>

            <Label
                as='a'
                color='green'
                image
                onClick={this.test}
              >
              <img src='hawk.png' /> Test
              </Label>


              <Label
                as='a'
                color='green'
                image
                onClick={this.set_bulk_search}
                // attached="left"
                fluid
              >
                <img src='hawk.png' />
                Back to search
              </Label>

              <div class="ui hidden section divider"></div>

              <Form onSubmit={this.onFormSubmit}>
                <Form.Field>
                
                  <label style={{color: 'white'}}>File input & upload</label>
                  
                  <Button as="label" htmlFor="file" type="button" animated="fade">
                    <Button.Content visible>
                      <Icon name="file" />
                    </Button.Content>
                    <Button.Content hidden>Choose a File</Button.Content>
                  </Button>
                  
                  <input
                    type="file"
                    id="file"
                    hidden
                    onChange={this.fileChange}
                  />
                  <Form.Input
                    fluid
                    // label="File Chosen: "
                    placeholder="Use the above bar to browse your file system"
                    readOnly
                    value={this.state.fileName}
                    // color='white'
                    style={{color:'white'}}
                    inverted
                    onChange={ (event) => {
                      this.setState({ days: event.target.value });
                    }} 
                  />

                  <Button style={{ marginTop: "20px" }} type="submit">
                    Upload
                  </Button>
                </Form.Field>
              </Form>
            </Tab.Pane>
          </div>
        ) : (<div></div>)
      }
      {
        this.state.activeButton === 'postSearch' ? 
        (
          <div>
            {this.state.bulk_search_results !== null ? (
            <div>
              <Label
                as='a'
                color='green'
                image
                onClick={this.set_bulk_search}
              >
              <img src='hawk.png' /> Back to search
              </Label>

              <Card.Group centered itemsPerRow="5" style={{ marginTop: "50px", textTransform: 'lowercase' }} className='domains'>
                {this.state.bulk_search_results.domains.map(domain => (
                  // <_Card payload={domain} key={domain.name}/>
                  <Card style={{backgroundColor:'black'}}>
                    <Card.Content>
                      <Card.Header as="a" href='https://www.google.com' target="_blank" style={{color:'white'}}>
                        <Label size='big' style={{'color': 'orange', 'backgroundColor':'transparent'}}>{domain.name}.eth</Label>
                      </Card.Header>
                      <Card.Meta style={{color:'white'}}>
                        Owner:
                        <a
                          as='a'
                          href={'https://etherscan.io/address/' + domain.owner}
                          target='_blank'
                          style={{color:'white'}}
                        >
                          {this.state.reverse_records[(domain.owner)] === null ? (" " + domain.owner.substr(0, 10)) : (' ' + this.state.reverse_records[(domain.owner)].substr(0, 10))}
                          {this.state.reverse_records[(domain.owner)] === null ? '...':'.eth'}
                        </a>
                      </Card.Meta>
                      <Card.Description style={{color:'white'}}>
                        {handleStatus(domain)}
                      </Card.Description>
                    </Card.Content>
                    <Rating
                      style={{backgroundColor:'gray'}}
                      icon='heart'
                      onRate={(event) => {
                        console.log(`i am a ratoooor`)
                      }}
                    />
                  </Card>    
                ))}
              </Card.Group>
            </div>
            ) : (<div></div>) }
          </div>
        ) : (<div></div>)
      }
    </div>
    )
  }
}