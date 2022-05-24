"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const port = process.env.PORT || 8000;
const app = express_1.default();
app.get('/', (req, res) => { res.send('Hello World from theWiseDev in Azure!!!'); });
app.listen(port, () => { console.log('Our App Is Up And Running on Azure.'); });
module.exports = app;
