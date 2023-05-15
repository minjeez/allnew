const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("sync-mysql");
const env = require("dotenv").config({ path: "../../.env" });

var connection = new mysql({
  host: process.env.host,
  user: process.env.user,
  password: process.env.password,
  database: process.env.database,
});

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/intro", (req, res) => {
  res.send("고객님의 건강과 행복을 기원하겠읍니다.");
});


app.get("/selectQuery", (req, res) => {
  const UsrId = req.query.UsrId;
  const result = connection.query("select * from UsrTbl where UsrId=?", [UsrId]);
  console.log(result);
  res.send(result);
});

app.post("/insert", (req, res) => {
    const { UsrId, Name, Addr, Favor } = req.body;
    const result = connection.query("insert into UsrTbl values (?, ?, ?, ?)", [UsrId, Name, Addr, Favor]);
    console.log(result);
    res.redirect('/selectQuery?UsrId='+req.body.UsrId)
});


app.post("/update", (req, res) => {
    const { UsrId, Name, Addr, Favor } = req.body;
    const result = connection.query("update user set Name=? where userid=?", [pw, id]);
    console.log(result);
    res.redirect('/selectQuery?userid='+req.body.id);
});


app.post("/delete", (req, res) => {
    const UsrId = req.body.UsrId;
    const result = connection.query("delete from UsrId where userid=?", [UsrId]);
    console.log(result);
    res.redirect('/select');
});


module.exports = app;