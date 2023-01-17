const AWS = require("aws-sdk");
const fs = require("fs");
const os = require("os");

const ssmClient = new AWS.SSM({
  apiVersion: "2014-11-06",
  region: "eu-west-2",
});

function setEnvValue(key, value) {
  // read file from hdd & split if from a linebreak to a array
  const ENV_VARS = fs.readFileSync("./backend/core/.env", "utf8").split(os.EOL);

  // find the env we want based on the key
  const target = ENV_VARS.indexOf(
    ENV_VARS.find((line) => {
      return line.match(new RegExp(key));
    })
  );

  // replace the key/value with the new value
  ENV_VARS.splice(target, 1, `${key}="${value}"`);

  // write everything back to the file system
  fs.writeFileSync("./backend/core/.env", ENV_VARS.join(os.EOL));
}

function getSSMStuff(path, memo = [], nextToken) {
  return ssmClient
    .getParametersByPath({
      Path: path,
      WithDecryption: true,
      Recursive: true,
      NextToken: nextToken,
      MaxResults: 10,
    })
    .promise()
    .then(({ Parameters, NextToken }) => {
      const newMemo = memo.concat(Parameters);
      return NextToken ? getSSMStuff(path, newMemo, NextToken) : newMemo;
    });
}

const Path = `/pop-api/`;

getSSMStuff(Path).then((results) => {
  if (results) {
    results.forEach((item) => {
      var key = item.Name.slice(Path.length);
      var value = item.Value;
      console.log(key, value);
      setEnvValue(key, value);
    });
  } else {
    console.log("Not getting the data!!");
  }
});
