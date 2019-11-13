---
layout: poster
title: 基于区块链的学历认证系统
date: 2018-06-02 16:20:14
tags: [BlockChain,Etherum,Node,Mysql]
---

# 基于区块链的学历认证系统
<!--more-->
目前学位证书由中心机构进行管理，并提供查询服务。一旦中心机构遭到恶意攻击，数据被篡改、增加或者删除，就会导致学位证书信息的完整性被破坏。而为了避免这种攻击，就需要对存储和管理设备进行大量的投入。

针对上述问题，本作品提供一种基于区块链的学位认证系统，本系统将学位证书默克尔哈希树树根信息发布在以太坊区块链上，以减少区块存储负担。能够通过智能合约对发布的信息进行增加、修改、查询等功能，采用分布式门限签名方案可以对学校发布的默克尔哈希树树根进行签名，也可以通过学生学位证书和一笔交易的Merkel Hash Root对具体交易信息进行验证。

本文构建基于论文区块链去中心化理念的学位认证系统，学历信息区块的构造机制、签名机制、共识算法确保学历信息的完整性和可溯源性；
设计了基于区块链的学历信息存储方式，利用Merkle哈希算法对每个学校的大学历信息进行压缩，将256bit的Merkle哈希树根存储于区块链中，大大减少了放入区块链上的数据；

建立了基于以太坊（Etherum）的智能合约机制，通由教育部授权各个学校具有使用智能合约的功能，并使各个学校可以对各个学校的毕业证书计算得到的默克尔哈希树树根进行添加、修改操作。

构建了多部门的门限签名方案，以防止签名密钥的信息泄露。将存储学历信息的公有链地址私钥信息分为n个子密钥，利用门限签名对交易进行签名；在智能合约中加入对数据的签名，该签名利用学校公开证书进行签名，验证者可以通过该签名验证数据的发布者身份，并采用门限签名方案防止签名密钥信息泄露；

实现多途径的学历认证方式，学校向学生颁发电子证书之后，可以由用人单位利用学校证书对电子学历证书进行验证，可以直接在公有链上进行验证，还可以利用身份证号等唯一标识信息在官方网站进行验证。

本作品创新性的将学历认证系统与区块链系统结合起来，增强了学历信息的可认证性和可追溯性，同时使得学历信息的认证查询得到极大的便
<!--more-->
#### 图片

![33.png](https://i.loli.net/2018/06/02/5b1254346a24f.png)
![111.png](https://i.loli.net/2018/06/02/5b1254388e350.png)
![3333.png](https://i.loli.net/2018/06/02/5b12543a3ecb8.png)
![123.png](https://i.loli.net/2018/06/02/5b12543b2cd97.png)

####此下面为一个简单sol智能合约代码

```sol
pragma solidity ^0.4.18;

contract FCERTContract {
    struct Education{
        string name;
        uint Mroot;
        uint Sign;
    }
    //Education[][] educate;
    mapping(uint=>Education)[100] public educate;
    mapping(uint=>uint) public num_cert;
    //uint[] num_cert;
    mapping(uint=>address) public Add; 
    uint num2;
    address public Ministry_of_Education;
    event e(string op,string name,uint Mroot,uint Sign);
	event d(string op,address Addr);
	event f(string op,uint number);
    /* Constructor */
    function FCERTContract() public {
        Ministry_of_Education=msg.sender;
        num2=0;
    }
    function newAdd(address school) public {
        if(msg.sender!=Ministry_of_Education)return;
        Add[num2]=school;
        num_cert[num2]=0;
        ++num2;
        emit d("new Address",school);
    }
    function DelAdd(uint num3) public {
        if(msg.sender!=Ministry_of_Education)return;
        if(num3>num2)return;
        delete Add[num3];
        emit f("delete Address",num3);
    }
    function newEdu(uint Snum,string name,uint Mroot,uint Sign) public {
        if(msg.sender!=Add[Snum])return;
        uint temp=num_cert[Snum];
        educate[Snum][temp].name=name;
        educate[Snum][temp].Mroot=Mroot;
        educate[Snum][temp].Sign=Sign;
        ++num_cert[Snum];
        emit  e("newEducation",name,Mroot,Sign);
    }
    function setEdu(uint numb,uint Snum,string name,uint Mroot,uint Sign) public {
        if(msg.sender!=Add[Snum])return;
        if(numb>=num_cert[Snum])return;
        educate[Snum][numb].name=name;
        educate[Snum][numb].Mroot=Mroot;
        educate[Snum][numb].Sign=Sign;
        emit e("setEducation",name,Mroot,Sign);
    }
    function getEdu(uint Snum,uint num) public return(uint ){
        return educate[Snum][num].Mroot;
    }
}
```



大约就是一个简单的授权功能，，然后写了个静态的展示网页，其实什么都没有，

![pic.png](https://i.loli.net/2018/06/02/5b1251b7743cf.png)

#### 然后这是一个 生成`Merkle`哈希树的`node` 脚本模块,用来生成树，



```javascript
var crypto = require('crypto');
var through = require('through');

var REGEXP = {
  'md5':       "^[0-9a-f]{32}$",
  'sha1':      "^[0-9a-f]{40}$",
  'ripemd160': "^[0-9a-f]{40}$",
  'sha256':    "^[0-9a-f]{64}$",
  'sha512':    "^[0-9a-f]{128}$",
  'whirlpool': "^[0-9a-f]{128}$",
  'DEFAULT':   "^$"
};

function Merkle (hashFunc, hashFuncName, useUpperCaseForHash) {

  var that = this;

  var resFunc = function () {
    return root();
  };

  var regexpStr = REGEXP[hashFuncName] || REGEXP.DEFAULT;
  if (useUpperCaseForHash) {
    // Use only capital letters if upper case is enabled
    regexpStr = regexpStr.replace('a', 'A').replace('f', 'F');
  }
  that.hashResultRegexp = new RegExp(regexpStr);
  that.leaves = [];
  that.treeDepth = 0;
  that.rows = [];
  that.nodesCount = 0;

  function feed(anyData) {
    var data = String(anyData);
    if(data && data.match(that.hashResultRegexp)){
      // Push leaf without hashing it since it is already a hash
      that.leaves.push(data);
    }
    else{
      var hash = hashFunc(data);
      if (useUpperCaseForHash) {
        hash = hash.toUpperCase();
      }
      that.leaves.push(hash);
    }
    return that;
  }

  function depth() {
    // Compute tree depth
    if(!that.treeDepth){
      var pow = 0;
      while(Math.pow(2, pow) < that.leaves.length){
        pow++;
      }
      that.treeDepth = pow;
    }
    return that.treeDepth;
  }

  function levels() {
    return depth() + 1;
  }

  function nodes() {
    return that.nodesCount;
  }

  function root() {
    return that.rows[0][0];
  }

  function level(i) {
    return that.rows[i];
  }

  function compute() {
    var theDepth = depth();
    if(that.rows.length == 0){
      // Compute the nodes of each level
      for (var i = 0; i < theDepth; i++) {
        that.rows.push([]);
      }
      that.rows[theDepth] = that.leaves;
      for (var j = theDepth-1; j >= 0; j--) {
        that.rows[j] = getNodes(that.rows[j+1]);
        that.nodesCount += that.rows[j].length;
      }
    }
  }

  function getNodes(leaves) {
    var remainder = leaves.length % 2;
    var nodes = [];
    var hash;
    for (var i = 0; i < leaves.length - 1; i = i + 2) {
      hash = hashFunc(leaves[i] + leaves[i+1]);
      if (useUpperCaseForHash) {
        hash = hash.toUpperCase();
      }
      nodes[i/2] = hash;
    }
    if(remainder === 1){
      nodes[((leaves.length-remainder)/2)] = leaves[leaves.length - 1];
    }
    return nodes;
  }
  
  function getProofPath(index, excludeParent) {
    var proofPath = [];

    for (var currentLevel = depth(); currentLevel > 0; currentLevel--) {
      var currentLevelNodes = level(currentLevel);
      var currentLevelCount = currentLevelNodes.length;

      // if this is an odd end node to be promoted up, skip to avoid proofs with null values
      if (index == currentLevelCount - 1 && currentLevelCount % 2 == 1) {
        index = Math.floor(index / 2);
        continue;
      }

      var nodes = {};
      if (index % 2) { // the index is the right node
        nodes.left = currentLevelNodes[index - 1];
        nodes.right = currentLevelNodes[index];
      } else {
        nodes.left = currentLevelNodes[index];
        nodes.right = currentLevelNodes[index + 1];
      }

      index = Math.floor(index / 2); // set index to the parent index
      if (!excludeParent) {
        proofPath.push({
          parent: level(currentLevel - 1)[index],
          left: nodes.left,
          right: nodes.right
        });
      } else {
        proofPath.push({
          left: nodes.left,
          right: nodes.right
        });
      }

    }
    return proofPath;
  }

  // PUBLIC

  /**
  * Return the stream, with resulting stream begin root hash string.
  **/
  var stream = through(
    function write (data) {
      feed('' + data);
    },
    function end () {
      compute();
      this.emit('data', resFunc());
      this.emit('end');
    });

  /**
  * Return the stream, but resulting stream will be json.
  **/
  stream.json = function () {
    resFunc = function() {
      return {
        root: root(),
        level: level(),
        depth: depth(),
        levels: levels(),
        nodes: nodes(),
        getProofPath: getProofPath
      };
    };
    return this;
  };

  /**
  * Computes merkle tree synchronously, returning json result.
  **/
  stream.sync = function (leaves) {
    leaves.forEach(function(leaf){
      feed(leaf);
    });
    compute();
    resFunc = function() {
      return {
        root: root,
        level: level,
        depth: depth,
        levels: levels,
        nodes: nodes,
        getProofPath: getProofPath
      };
    };
    return resFunc();
  };

  /**
  * Computes merkle tree asynchronously, returning json as callback result.
  **/
  stream.async = function (leaves, done) {
    leaves.forEach(function(leaf){
      feed(leaf);
    });
    compute();
    resFunc = function() {
      return {
        root: root,
        level: level,
        depth: depth,
        levels: levels,
        nodes: nodes,
        getProofPath: getProofPath
      };
    };
    done(null, resFunc());
  };

  return stream;
}

module.exports = function (hashFuncName, useUpperCaseForHash) {
  return new Merkle(function (input) {
    if (hashFuncName === 'none') {
      return input;
    } else {
      var hash = crypto.createHash(hashFuncName);
      return hash.update(input).digest('hex');
    }
  }, hashFuncName,

  // Use upper case y default
  useUpperCaseForHash !== false);
};


```

#### 这是一个把生成的树插入到本地的`MySQL`数据库中，

```javascript
var mysql = require('mysql');
var merkle=require("./merkle.js");
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '123',
  database : 'stud'
});
 
connection.connect();
 
connection.query('SELECT * from websites', function (error, results, fields) {
  if (error) throw error;
  for(var i=0;i<5;i++){
    console.log('The solution is: ', results[i]);
  }
  var arr=[];
  
  for(var i=0;i<results.length;i++){
        var info=results[i].id.toString()+results[i].name+results[i].sex.toString()+results[i]['enterDay']+results[i]['leaveDay']+results[i]['schoolName']+results[i]['major']+results[i]['certID'];
        arr.push(info);
  }
  
console.log(arr);

var tree=merkle('sha1').sync(arr);
var abi=[ { "constant": false, "inputs": [ { "name": "school", "type": "address" } ], "name": "newAdd", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Ministry_of_Education", "outputs": [ { "name": "", "type": "address", "value": "0xe7ea891e572345a05a7c1e8cfd64acba914db18c" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "numb", "type": "uint256" }, { "name": "Snum", "type": "uint256" }, { "name": "name", "type": "string" }, { "name": "Mroot", "type": "uint256" }, { "name": "Sign", "type": "uint256" } ], "name": "setEdu", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "educate", "outputs": [ { "name": "name", "type": "string", "value": "" }, { "name": "Mroot", "type": "uint256", "value": "0" }, { "name": "Sign", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "num3", "type": "uint256" } ], "name": "DelAdd", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "num_cert", "outputs": [ { "name": "", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "Add", "outputs": [ { "name": "", "type": "address", "value": "0xc06da6e18c352a26512aa42ca050aa85a31f024c" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "Snum", "type": "uint256" }, { "name": "name", "type": "string" }, { "name": "Mroot", "type": "uint256" }, { "name": "Sign", "type": "uint256" } ], "name": "newEdu", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "op", "type": "string" }, { "indexed": false, "name": "name", "type": "string" }, { "indexed": false, "name": "Mroot", "type": "uint256" }, { "indexed": false, "name": "Sign", "type": "uint256" } ], "name": "e", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "op", "type": "string" }, { "indexed": false, "name": "Addr", "type": "address" } ], "name": "d", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "op", "type": "string" }, { "indexed": false, "name": "number", "type": "uint256" } ], "name": "f", "type": "event" } ];
console.log('the address of contract is      ')
 console.log(abi);
 console.log('the Mroot of Merkle  hash tree is ')
 console.log(tree.root());
 /*var i=tree.depth();
 for(var j=0;j<i;j++){
   console.log(tree.level(j))
 }*/
 console.log('-----get Merkle hash tree root from Local Mysql-----')
 console.log(tree.root())
 
 
 // 修改某位同学的信息
  
/*var name='shelock';
var modSql = 'UPDATE websites SET major = ?,schoolName = ? WHERE name = ?';
var modSqlParams = ['菜鸟移动站', 'https://yeahyeah.com',name];
//改
connection.query(modSql,modSqlParams,function (err, result) {
   if(err){
         console.log('[UPDATE ERROR] - ',err.message);
         return;
   }        
  console.log('--------------------------UPDATE----------------------------');
  console.log('UPDATE affectedRows',result.affectedRows);
  console.log('-----------------------------------------------------------------\n\n');
});*/
 
connection.end();
 
})

```

其实这时候不会用`node`的`vue`框架，不然其实可以把整个系统做完，有前端，有后端，然而，，，,



#### 参考资料

\- [Merkel-tree-solidity-github-js](https://github.com/ameensol/merkle-tree-solidity)

\- [Merkel-nodejs模块](https://www.helplib.com/GitHub/article_101101)

\- [图文详解Merkle TREE](https://my.oschina.net/tantexian/blog/839601)

\- [国外学历认证网站实例](https://smartdiploma.io/)

\- [GitBook学历认证描述](https://yeasy.gitbooks.io/blockchain_guide/content/app_dev/chaincode_example04.html)

\- [？？？DappStudentID](https://www.stateofthedapps.com/dapps/smart-student-id)

\- [私有链搭建操作指南](https://my.oschina.net/u/2349981/blog/865256)

\- [Geth搭建私有链](https://blog.csdn.net/Vinsuan1993/article/details/75208203)

\- [Windows系统以太坊区块链私链的搭建启动、数据抓取、浏览器数据显示](http://blog.csdn.net/vinsuan1993/article/details/75208203)

\- [Web3 JavaScript app API for 0.2x.x](https://github.com/ethereum/wiki/wiki/JavaScript-API)

\- [https://blog.csdn.net/chenyufeng1991/article/details/53458175]