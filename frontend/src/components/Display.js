import _ from 'lodash'
import React from 'react'
import { Table } from 'semantic-ui-react'


function exampleReducer(state, action) {
  switch (action.type) {
    case 'CHANGE_SORT':
      if (state.column === action.column) {
        return {
          ...state,
          payload: state.payload.slice().reverse(),
          direction:
            state.direction === 'ascending' ? 'descending' : 'ascending',
        }
      }

      return {
        column: action.column,
        payload: _.sortBy(state.payload, [action.column]),
        direction: 'ascending',
      }
    default:
      throw new Error()
  }
}

function TableExampleSortable() {
  const [state, dispatch] = React.useReducer(exampleReducer, {
    column: null,
    payload: this.props.payload,
    direction: null,
  })
  const { column, payload, direction } = state

  return (
    <Table sortable celled fixed>

      <Table.Header>
        <Table.Row>
          <Table.HeaderCell
            sorted={column === 'name' ? direction : null}
            onClick={() => dispatch({ type: 'CHANGE_SORT', column: 'name' })}
          >
            Name
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === 'expiration' ? direction : null}
            onClick={() => dispatch({ type: 'CHANGE_SORT', column: 'expiration' })}
          >
            Expiration
          </Table.HeaderCell>
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {payload.map(({ name, expiration }) => (
          <Table.Row key={name}>
            <Table.Cell>{name}</Table.Cell>
            <Table.Cell>{expiration}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>

    </Table>
  )
}

export default TableExampleSortable
