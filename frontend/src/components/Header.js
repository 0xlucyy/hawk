import React, { Component } from 'react'
import { Menu, Input } from 'semantic-ui-react'
import { Link } from "react-router-dom"


export default class _Header extends Component {
  constructor(props) {
    super(props);
    // this.state = {activeItem: this.props.active};
    this.handleItemClick = this.props.handler.bind(this);
    // this.active_item = this.props.active;
  }

  state = {
    gas_costs: null,
    // active_item: null,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  load_gas_costs = async (e, value) => {
    e.preventDefault();

    console.log(`Loading gas costs from etherscan....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/getETHGasCosts`);
    const gas_costs = await response.json();
    this.setState({ gas_costs });
  };

  another_try = async (e, value) => {
    console.log(`value: ${value}`)
    console.log(`JSON: ${JSON.stringify(value.name)}`)
    e.preventDefault();
    // <div>{await this.handleItemClick()}</div>
    this.setState({ active_item: value.name })
  }

  render() {
    // const { activeItem } = this.props.active

    return (
      <div id='header'>
        <Menu inverted>

          <Menu.Item
            as='h2'
            style={{ 'color':'green'}}
            attached='top'
            textAlign='center'
            className='header'
            name='ENS HAWK'
          />

          <Menu.Item
            as={Link}
            to="/"
            name='home'
            // active={this.state.activeItem === 'home'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='expiring'
            // active={this.state.activeItem === 'expiring'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='all'
            // active={this.state.activeItem === 'all'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='bulk search'
            active={this.state.active_item === 'bulk search'}
            onClick={this.handleItemClick}
            // {...this.another_try}'
            // onClick={this.another_try}
          />{this.another_try}
          <Menu.Menu position='right'>
            <Menu.Item>
              <Input icon='search' placeholder='Search...' />
            </Menu.Item>
          </Menu.Menu>

          {/* <Menu.Item
            as={Link}
            to="/name"
            name='names'
            // active={this.state.activeItem === 'contact'}
            onClick={this.handleItemClick}
            // target='_blank'
          /> */}
        </Menu>
      </div>
    )
  }
}
