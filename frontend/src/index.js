
import App from './App';
import Table from './components/Table.js';
import reportWebVitals from './reportWebVitals';



import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    // <App />
  // </React.StrictMode>


  <BrowserRouter>
  <Routes>
    <div></div>
    <Route path="/" element={<App />}>
      {/* <Route index element={<Home />} /> */}
      <Route path="tables" element={<Table />} />
      {/* <Route path="contact" element={<Contact />} /> */}
      {/* <Route path="*" element={<NoPage />} /> */}
    </Route>
  </Routes>
</BrowserRouter>

);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
