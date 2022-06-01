import express from 'express'
const port = process.env.PORT || 8000
const app = express()

app.get('/', (req, res) => { res.send('Hello World from theWiseDev in Azure!!!') })

app.listen(port, () => { console.log('Our App Is Up And Running on Azure.') })
module.exports = app
