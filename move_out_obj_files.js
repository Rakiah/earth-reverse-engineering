"use strict"

const fs = require('fs-extra');
var exec = require('child_process').exec;
const path = require('path');

async function run() {
	var inputFolder = process.argv[2];
	var outputFolder = process.argv[3];

	fs.ensureDirSync(outputFolder);
	var files = await executeAsync(`find ${inputFolder} -type f -name *.obj`);
	
	files = files.split("\n").filter((el) => el != "");
	for (const file of files)
    {
		await executeAsync(`mv ${file} ${outputFolder}`);
    }
}

async function executeAsync(command)
{
	return new Promise((resolve, reject) =>
	{
		exec(command, {maxBuffer: 1024 * 100000}, function(error, stdout, stderr) {
			console.log(`${stderr}`);

			if (error !== null)
				reject(error);
			else
				resolve(stdout);
		});
	});
}

(async function program() {
	await run();
})().then(() => {
	process.exit(0);
}).catch(e => {
	console.error(e);
	process.exit(1);
});
