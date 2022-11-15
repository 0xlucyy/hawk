import React, { Component } from 'react'
import { Menu, Header, Image } from 'semantic-ui-react'
import { Link } from "react-router-dom"


export default class _Header extends Component {
  constructor(props) {
    super(props);
    // this.state = {activeItem: this.props.active};
    this.handleItemClick = this.props.handler.bind(this);
  }

  render() {
    // const { activeItem } = this.props.active

    return (
      <div id='header'>
        <Menu inverted vertical>
          <Header
            inverted
            as='h2'
            attached='top'
            textAlign='center'
            className='header'
            color='green'
          >
            ENS Hawk API
          </Header>

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
            to="/contacts/1"
            name='contact'
            // active={this.state.activeItem === 'contact'}
            onClick={this.handleItemClick}
            // target='_blank'
          />
        </Menu>
      </div>
    )
  }
}
