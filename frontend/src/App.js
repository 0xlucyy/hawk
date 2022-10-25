import React from 'react'
import ReachDOM from 'react-dom'

const App = () => {
    return(
        <div>
            <h1>Hello</h1>
            <h3>In frontend/src/app.js, bundled in public/bundle.js</h3>
        </div>
    )
}

// class App extends React.Component {
//     render() {
//         return(
//             <div>
//                 <h1>is it changing</h1>
//                 <h3>I am in</h3>
//             </div>
//         )
//     }
// }

ReachDOM.render(<App />, document.getElementById("root"))

// export default App;