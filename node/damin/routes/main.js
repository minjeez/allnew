const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env" });
const mongoose = require('mongoose');

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// nodata
function template_nodata(res) {
    res.writeHead(200);
    var template = `
    <!doctype html>
    <html>
    <head>
        <title>Result</title>
        <meta charset="utf-8">
        <link type="text/css" rel="stylesheet" href="mystyle.css" />
    </head>
    <body>
        <h3>데이터가 존재하지 않습니다.</h3>
    </body>
    </html>
    `;
    res.end(template);
}

function template_result(result, res) {
    res.writeHead(200);
    var template = `
    <!doctype html>
    <html>
    <head>
        <title>Result</title>
        <meta charset="utf-8">
        <link type="text/css" rel="stylesheet" href="mystyle.css" />
    </head>
    <body>
    <table border="1" style="margin:auto;">
    <thead>
        <tr><th>회원 ID</th><th>&nbsp;비밀번호&nbsp;</th><th>&nbsp;&nbsp;이름&nbsp;&nbsp;</th><th>주소</th><th>&nbsp;&nbsp;자주방문한장소&nbsp;&nbsp;</th>
    </thead>
    <tbody>
    `;
    for (var i = 0; i < result.length; i++) {
        template += `
    <tr>
        <td>${result[i]['id']}</td>
        <td>${result[i]['pw']}</td>
        <td>${result[i]['name']}</td>
        <td>${result[i]['addr']}</td>
        <td>${result[i]['favor']}</td>
    </tr>
    `;
    }
    template += `
    </tbody>
    </table>
    </body>
    </html>
    `;
    res.end(template);
}

// define schema
var taxi_Schema = mongoose.Schema({
    id: Number,
    // pw: String,
    usr: String,
    cartype: String,
    area: String,
    avl: Number
}, {
    versionKey: false
})

//MY SQL > MONGO Insert 위한 Select
function resselect_result(req) {
    const result = connection.query('SELECT * FROM taxitbl where availability = 1');
    return result;
}

// create model with mongodb collection and schema
var Taxi = mongoose.model('taxi', taxi_Schema);

// mongo insert
app.get('/mongoinsert', function (req, res) {
    let result = resselect_result(req)
    let flag = 0

    for (var i = 0; i < result.length; i++) {
        var id = result[i].id;
        var usr = result[i].usr;
        var cartype = result[i].cartype;
        var area = result[i].area;
        var avl = result[i].availability;

        var taxi = new Taxi({ 'id': id, 'usr': usr, 'cartype': cartype, 'area': area, 'avl': availability })

        console.log(taxi)

        taxi.save(function (err, silence) {
            if (err) {
                flag = 1;
                return;
            }
        })
        if (flag) break;
    }

    if (flag) {
        console.log('err')
        // res.status(500).send('insert error')
        res.send({ "ok": false, "result": [taxi], "service": "mongoinsert" });
    } else {
        // res.status(200).send("Inserted")
        res.send({ "ok": true, "result": [taxi], "service": "mongoinsert" });
    }

});

// list
app.get('/list', function (req, res, next) {
    Taxi.find({}, function (err, docs) {
        if (err) console.log('err')
        // res.send(docs)
        let template = `
        <html>
          <head>
            <title>Taxi Availability</title>
            <meta charset="utf-8">
            <style>
              table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
              }
              th, td {
                padding: 10px;
                text-align: left;
              }
              th {
                background-color: #4CAF50;
                color: white;
              }
            </style>
          </head>
          <body>
            <h1>Taxi Availability</h1>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Driver Name</th>
                  <th>Car Type</th>
                  <th>Area</th>
                  <th>Availability</th>
                </tr>
              </thead>
              <tbody>
                ${docs.map((taxi) => `
                  <tr>
                    <td>${taxi.id}</td>
                    <td>${taxi.usr}</td>
                    <td>${taxi.cartype}</td>
                    <td>${taxi.area}</td>
                    <td>${taxi.availability}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </body>
        </html>
      `;

        res.send(template);


    })
});


// User Login
app.post('/login', (req, res) => {
    const { id, pw } = req.body;
    const user = connection.query("select * from usrtbl where id=? and pw=?", [id, pw]);
    // console.log(result);
    if (user.length == 0) {
        // res.send({ 'ok': true, 'user': id, 'message': '로그인에 실패하였습니다' })
        res.redirect('error.html')
    }
    if (id == '01025884317') {
        console.log(id + " => Administrator Logined")
        // res.send({ 'ok': true, 'user': user, 'job': 'Admin Logined' });
        res.redirect('admin.html?id=' + id)
    } else {
        console.log(id + " => User Logined")
        // res.send({ 'ok': true, 'user': user, 'job': '로그인 완료' });
        res.redirect('main.html?id=' + id)
    }
});

// User Register
app.post('/register', (req, res) => {
    const { id, pw, name, addr, favor } = req.body;
    if (id == "" || pw == "" || name == "") {
        res.send({ 'ok': false, 'error': '필수값을 입력하세요' });
        // res.redirect('register.html')
    } else {
        let result = connection.query("select * from usrtbl where id=?", [id]);
        if (result.length > 0) {
            res.writeHead(200);
            var template = `
        <!doctype html>
        <html>
        <head>
            <title>Error</title>
            <meta charset="utf-8">
        </head>
        <body>
            <div>
                <h3 style="margin-left: 30px">Registrer Failed</h3>
                <h4 style="margin-left: 30px">이미 존재하는 아이디입니다.</h4>
                <a href="register.html" style="margin-left: 30px">다시 시도하기</a>
            </div>
        </body>
        </html>
        `;
            res.end(template);
        } else {
            result = connection.query("insert into usrtbl values (?, ?, ?, ?, ?)", [id, pw, name, addr, favor]);
            console.log(result);
            // res.send({ 'ok': true, 'user info': id, pw, name, addr, favor, 'job': '가입 완료' });
            res.redirect('/');
        }
    }
})

// User Select in Admin
app.get('/select', (req, res) => {
    const result = connection.query('select * from usrtbl');
    console.log(result);
    // res.send(result);
    if (result.length == 0) {
        template_nodata(res)
    } else {
        template_result(result, res);
    }
})

// User SelectQuery in Admin
app.get('/selectQuery', (req, res) => {
    const id = req.query.id;
    if (id == "") {
        res.send({ 'ok': false, 'error': 'ID를 입력하세요.' })
        // res.write("<script>alert('ID를 입력하세요.')</script>");
    } else {
        const result = connection.query("select * from usrtbl where id=?", [id]);
        console.log(result);
        // res.send(result);
        if (result.length == 0) {
            template_nodata(res)
        } else {
            template_result(result, res);
        }
    }
})

// User Update
app.post('/update', (req, res) => {
    const { id, pw, addr, favor } = req.body;
    if (id == "" || pw == "") {
        res.send({ 'ok': false, 'error': 'ID와 Password를 입력하세요.' })
    } else {
        const result = connection.query("select * from usrtbl where id=?", [id]);
        console.log(result);
        // res.send(result);
        if (result.length == 0) {
            template_nodata(res)
        } else {
            const result = connection.query("update usrtbl set pw=?, addr=?, favor=? where id=?", [pw, addr, favor, id]);
            console.log(result);
            // res.send({ 'ok': true, 'user info': result, 'job': '업데이트 완료' });
            res.redirect('/selectQuery?id=' + id);
        }
    }
})

// User Delete in Admin
app.post('/delete', (req, res) => {
    const id = req.body.id;
    if (id == "") {
        res.send({ 'ok': false, 'error': 'ID를 입력하세요.' })
    } else {
        const result = connection.query("select * from usrtbl where id=?", [id]);
        console.log(result);
        // res.send(result);
        if (result.length == 0) {
            template_nodata(res)
        } else {
            const result = connection.query("delete from usrtbl where id=?", [id]);
            console.log(result);
            res.send({ 'ok': true, 'user info': result, 'job': '삭제 완료' });
            // res.redirect('/select');
        }
    }
})

// 택시 호출하기
app.get('/call', (req, res) => {
    const { area, cartype } = req.query;
    let result = connection.query("select id, usr from taxitbl where area=? and cartype=?", [area, cartype]);
    console.log(result);
    res.writeHead(200);
    var template = `
  <!doctype html>
  <html>
  <head>
    <title>Result</title>
    <meta charset="utf-8">
  </head>
  <body>
   <table border="1" margin:auto; text-align:center;>
     <tr>
       <th>&nbsp;&nbsp;&nbsp;&nbsp;기사님 전화번호&nbsp;&nbsp;&nbsp;&nbsp;</th>
       <th>&nbsp;&nbsp;&nbsp;&nbsp;기사님 성함&nbsp;&nbsp;&nbsp;&nbsp;</th>
     </tr>
   `;
    for (var i = 0; i < result.length; i++) {
        template += `
     <tr>
       <th>${result[i]['id']} <a href="call.html">전화하기</a></th>
       <th>${result[i]['usr']}</th>
     </tr>
    `
    }
    template += `
     </table>
     <br>
     <a href="main.html">다시 호출하기</a>
  </body>
  </html>
 `;
    res.end(template);
});

module.exports = app;