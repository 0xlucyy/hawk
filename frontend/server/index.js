const express = require('express')
const app = express()
const port = 3000
const path = require('path')
const React = require('react')

import App from "../src/app.js"

var ReactDOMServer = require('react-dom/server')


app.use("/static", express.static(path.join(__dirname, '..', 'public')))

app.get("/", (req, res) => {
    const component = ReactDOMServer.renderToString(<App />)

    res.send(<App />)
})

app.listen(port, () => {
        console.log(`server now listening at http://localhost:${port}`)
    }
)






// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   // <React.StrictMode>
//     <App />
//   // </React.StrictMode>
// );