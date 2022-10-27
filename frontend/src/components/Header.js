import React, { Component } from 'react'
import { Menu, Header, Image } from 'semantic-ui-react'
import { Link } from "react-router-dom"


export default class _Header extends Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.handleItemClick = this.props.handler.bind(this);
  }

  render() {
    const { activeItem } = this.state

    return (
      <div>
        <Header
          inverted
          as='h2'
          attached='top'
          textAlign='center'
          className='header'
          color='green'
        >
          ENS Hawk
        </Header>

        <Menu inverted pointing vertical>
          <Menu.Item
            as={Link}
            to="/"
            name='home'
            active={activeItem === 'home'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='expiring'
            active={activeItem === 'expiring'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='all'
            active={activeItem === 'all'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/contacts/1"
            name='contact'
            active={activeItem === 'contact'}
            onClick={this.handleItemClick}
            // target='_blank'
          />
        </Menu>
      </div>
    )
  }
}
