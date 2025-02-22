"use strict";

// centers and scales all *.obj and saves results as *.2.obj
// can also keep 3d viewers from jittering

const fs = require('fs');
const readline = require('readline');
const path = require('path');

module.exports = function scaleMoveObj(file_in, file_out) {
	const SCALE = 1;

	return new Promise((resolve, reject) =>
	{
		try
		{
			if (fs.existsSync(file_out)) {
				fs.unlinkSync(file_out);
			}

			const io = readline.createInterface({
				input: fs.createReadStream(file_in),
				terminal: false,
			});

			let min_x = Infinity, max_x = -Infinity;
			let min_y = Infinity, max_y = -Infinity;
			let min_z = Infinity, max_z = -Infinity;

			io.on('line', line => {
				if (!/^v /.test(line))
					return;
				let [x, y, z] = line.split(' ').slice(1).map(parseFloat);
				min_x = Math.min(x, min_x);
				min_y = Math.min(y, min_y);
				min_z = Math.min(z, min_z);
				max_x = Math.max(x, max_x);
				max_y = Math.max(y, max_y);
				max_z = Math.max(z, max_z);
			}).on('close', () => {
				const center_x = (max_x + min_x) / 2;
				const center_y = (max_y + min_y) / 2;
				// const center_z = (max_z + min_z) / 2;
				const distance_x = Math.abs(max_x - min_x);
				const distance_y = Math.abs(max_y - min_y);
				// const distance_z = Math.abs(max_z - min_z);
				const max_distance = Math.max(distance_x, distance_y/*, distance_z*/);

				const io = readline.createInterface({
					input: fs.createReadStream(file_in),
					output: fs.createWriteStream(file_out),
				});

				io.on('line', line => {
					if (!/^v /.test(line))
						return io.output.write(`${line}\n`);
					let [x, y, z] = line.split(' ').slice(1).map(parseFloat);
					x = (x - center_x) / max_distance * SCALE;
					y = (y - center_y) / max_distance * SCALE;
					// z = (z - center_z) / max_distance * SCALE;
					io.output.write(`v ${x} ${y} ${z}\n`);
				}).on('close', () => {
					resolve();
				});
			});
		}
		catch (error) {
			reject(error);
		}
	});
}
