const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const router = express.Router();
const app = express();
const mysql = require('mysql2/promise')
const fs = require('fs')

app.use(cors())

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.listen(8080);

router.post('/data', async (req, res)=>{

    const data = JSON.parse(JSON.stringify(req.body))
    console.log(data)
    try{
        const connection = await mysql.createConnection({host:'localhost', user: 'root', database: 'data'});
        await connection.execute("INSERT INTO `data`(`IP`, `NAME`, `TIMESTAMP`, `DATA`) VALUES (?,?,?,?)", [
            data.ip,
            data.name,
            data.timestamp,
            data.data
        ]);
        await connection.end()
        res.status(200).send('')
    }
    catch (error){
        const filename = data.ip+'_'+data.timestamp.replace(' '&&':', '_')
        fs.appendFile(`./backups/${filename}.txt`, data.data, (err)=>{
            if (err) throw err
            console.log(`file created at ${data.timestamp}`)
        })
        res.status(200).send('')
    }
});

app.use("/", router);