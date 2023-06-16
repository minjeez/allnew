const express = require('express');
const bodyParser = require('body-parser');
const env = require('dotenv').config({ path: "../../.env" });
const axios = require('axios')

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


app.get('/first_search_RCP', (req, res) => {
    const first_RCP_NM = req.query.first_RCP_NM;
    axios
        .get('http://192.168.1.163:3000/first_search_RCP', { params: { first_RCP_NM } })
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/search_RCP', (req, res) => {
    const RCP_NM_name = req.query.RCP_NM_name;
    axios
        .get('http://192.168.1.163:3000/search_RCP', { params: { RCP_NM_name } })
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/Psearch_RCP_process', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/Psearch_RCP_process')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/Regex', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/Regex')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/firstmatch', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/firstmatch')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/secondmatch', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/secondmatch')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/lastmatch', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/lastmatch')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/singo', (req, res) => {
    const args = req.query.args;
    axios
        .get('http://192.168.1.163:3000/singo', { params: { args } })
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/foodListCkeck', (req, res) => {
    const args = req.query.args;
    axios
        .get('http://192.168.1.163:3000/foodListCkeck', { params: { args } })
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/showRCP', (req, res) => {
    axios
        .get('http://192.168.1.163:3000/showRCP')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

// app.get('/foodDBget', (req, res) => {
//     axios
//         .get('http://192.168.1.163:3000/foodDBget')
//         .then(response => {
//             console.log(`statusCode : ${response.status}`)
//             console.log(response.data)
//             res.send(response.data)
//         })
//         .catch(error => {
//             console.log(error)
//         })
// })

// app.get('/arrangeCode', (req, res) => {
//     axios
//         .get('http://192.168.1.163:3000/arrangeCode')
//         .then(response => {
//             console.log(`statusCode : ${response.status}`)
//             console.log(response.data)
//             res.send(response.data)
//         })
//         .catch(error => {
//             console.log(error)
//         })
// })

app.get('/search_all', (req, res) => {
    const RCP_NM_name = req.query.RCP_NM_name;
    axios
        .get('http://192.168.1.163:3000/search_all', { params: { RCP_NM_name } })
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

module.exports = app;